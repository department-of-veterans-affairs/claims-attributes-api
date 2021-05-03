# Claims Attributes API

The Claims Attributes API takes in a JSON array of free-text, disability-related medical issues (called contentions) and returns the most likely official classifications and labels in a JSON array containing the below pieces of information. (Definitions are provided by Appendix C of the [M21-1 Adjudication Procedures Manual](https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000036570/Appendix-C.-Index-of-Claim-Attributes)
The return payload is a JSON array with the following pieces of information, with one entry per passed-in contention:

- _Classification code_: The numeric code for the official VA disability term
- _Special issues_: Flags that apply to specific contentions
- _Flashes_: Flags that apply to certain claimants

These classifications and labels are then used to ensure claims are processed quickly and accurately according to the appropriate review processes and offices.

_NOTE_: This API does not write any information to any system of record. It only returns features according to the learning model, which the caller can then determine how to use, such as adding them to disability compensation claims before submitting them to the VA.

## Background

Around 1.5 million Veterans apply for disability compensation benefits each year by submitting an Application for Disability Compensation ([21-526EZ](https://www.va.gov/find-forms/about-form-21-526ez/)), on which they indicate what disabilities they’d like to claim. Applicants frequently write disability symptoms that don’t match VA’s official list of symptoms. For example, a Veteran may write “ringing in my ears” as a disability, but VA only recognizes “hearing loss” as an official symptom.
The Claims Attributes API helps translate this free text into usable, official contentions, thus speeding up claims processing by:

- Identifying Classification
  The step of translating free-text into the official VA term is required before a claim can be established and assessed, which can cause delays. The Claims Attributes API helps avoid this delay by automatically making this translation.

- Identifying Special Issues and Flashes

  Some claims require particular regional office or specialist’s review. The Claims Attributes API identifies probable special issues and flashes related to a contention, allowing early identification and faster processing of claims that require specific reviews or processes. For example, claims with contentions associated with Agent Orange exposure must be reviewed by only certain regional offices, and assigning a special issue for Agent Orange will speed up this review by ensuring the claim reaches the correct office.

- Centralizing Information

  The Claims Attributes API pulls classifications from a single, machine-learning model, saving time and providing increased accuracy over the previously-used models that were deployed locally. Over time, we update and improve our model to benefit all parties.

## Technical Overview

This API uses a machine-learning model to match free-text contentions to the most likely official classifications and labels. Our machine-learning model is trained on millions of previously completed, anonymized disability claims, and is updated for greater accuracy when new information is available.

### Inputs and outputs

The Claims Attributes API is passed JSON payload object with a single member entitled `claim_text`, which is an array of free-text values. One example source of this data is each row of the `Current Disability(ies)` field of section IV (Claim Information) from the 21-526EZ form.

The API then passes each item in the array one at a time through the machine-learning model and outputs an object with a single `contentions` property that maps to an array with an entry for each inputted contention.

Each entry in this array contains:

- The original free-form claim text
- An array of flashes identified based on this claim text
- An array of special issues identified based on this claim text

- The classification that our model identified based on this claim text. This is further broken down by the code itself, a percentage confidence, and the text of the classification code.

_NOTE_: This API does not write any information to any system of record. It only returns features according to the learning model, which the caller can then determine how to use, such as adding them to disability compensation claims before submitting them to the VA.

### Structure

The Claims Attributes API is exposed to callers as a single service, but internally, it is broken down into three sub-components:

1. Contention classification
2. Special issue identification, and
3. Flash identification
   We will describe each sub-component below and where / how it gets its data.

#### Contention Classification

To establish the classification code and description, we first transform the free-text contentions into numeric vectors using a locally stored copy of a [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) transformation that has been trained with data from millions of previous claims. Our classifier then turns these numeric vectors into the appropriate classifications.
For this process, the API uses a locally stored copy of a previously trained Multi-Class Logistic Regression model to make the predictions. This model has been trained with data from past benefit claims to infer the relationship between the contention a Veteran wrote down on the form and the classification a VA employee ultimately assigned to it.
The following table shows an example of translating free-text contentions to numeric vectors and then formal classifications.
| Inputted Free-text Contentions | Numeric Vectors | Classifications |
| -------------------------------------- | ------------------ | ----------------------------------------------- |
| Ringing in my ear | [0.2, 3.4, …, 2.3] | code: 3140, text: hearing loss, confidence: .97 |
| Skin condition because of homelessness | [1.3, .3, …, 1.7]] | code: 9016, text: skin, confidence: .97 |

#### Flash Identification

Flashes are attributes related to the claimant and appended to a claim. The flashes sub-component receives a given list of contentions and determines whether any flashes apply by performing [an edit distance analysis](https://en.wikipedia.org/wiki/Edit_distance#:~:text=In%20computational%20linguistics%20and%20computer,one%20string%20into%20the%20other) between the contention and phrases known to be related to our selected list of flashes:

- Hardship
- Seriously Injured/Very Seriously Injured
- Terminally Ill
- Homeless
- Purple Heart
- POW
- Medal of Honor
- Amyotrophic Lateral Sclerosis
- Emergency Care
  If it finds a phrase that is matching or close to matching (such as if there is a typo in the free-text contention), it adds the flash.

For example, if the flashes sub-component receives “skin condition because of homelessness” as a free-text contention, it may apply the “Homeless” flash.

Our selected flashes list is not a complete list of existing flashes. To view the comprehensive list of flashes and their descriptions, see [here](https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000036570/Appendix-C-Index-of-Claim-Attributes?query=Appendix%20C.%20Index%20of%20Claim%20Attributes#2).

#### Special Issue Identification

Special issues are attributes appended to a claim to help identify special processing considerations. The special issues sub-component receives a contention and determines whether any special issues apply by performing an [an edit distance analysis](https://en.wikipedia.org/wiki/Edit_distance#:~:text=In%20computational%20linguistics%20and%20computer,one%20string%20into%20the%20other) between the contention and phrases related to these special issues:

- ALS (Amyotrophic Lateral Sclerosis)
- AOOV (Agent Orange outside of Vietnam)
- AOIV (Agent Orange in Vietnam)
- ASB (Asbestos)
- GW (Gulf War)
- HEPC (Hepatitis C)
- HIV (Human Immunodeficiency Viruses)
- MG (Mustard Gas)
- MST Military Sexual Trauma
- POW (Prisoner of War)
- PTSD/1 (combat experience)
- PTSD/2 (non-combat PTSD)
- PTSD/3 (personal trauma)
- RDN (Radiation)
- SARCO (Sarcoidosis)
- TBI (Traumatic Brain Injury)
- C123 (C-123 Aircraft, related to AO)

If it finds a phrase that is matching or close to matching (such as if there is a typo in the free-text contention), it adds the special issue or issues.
For example, if the special issues service receives “p.t.s.d from gulf war” as a free-text contention, it may apply the “PTSD/1” special issue.
