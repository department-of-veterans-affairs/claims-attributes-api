# Claims Attributes API

The Claims Attributes API is a RESTful service that takes in a JSON-formatted array of free-text descriptions of disability-associated medical issues (“contentions”) and uses a machine learning model to identify statistically-likely associated classifications and labels.

The return payload is a JSON array with the following pieces of information, with one entry per passed-in contention:

- A formal numeric classification code
- An array of labels representing facts about the contention itself (“special issues”)
- An array of labels representing facts about the claimant (“flashes”), and

This API does not write any information to any system of record, it simply returns features that its model has deemed relevant, which the caller can then determine how to use.

Its primary consumer at present is the Benefits Claims API, which calls into the service prior to claim establishment. The Benefits Claims API then uses the information returned by the Claims Attributes API to attach classification, special issues, and flashes to the contentions within the Corporate Database.

## Background

Around 1.5 million Veterans apply for disability compensation benefits each year. To do so, they submit an application, the Application for Disability Compensation ([21-526EZ](https://www.va.gov/find-forms/about-form-21-526ez/)), in which they indicate what disabilities they’d like to claim. Applicants frequently write disability symptoms that don’t match VA’s list of ‘official’ symptoms: a Veteran can write “ringing in my ears” on a claim, but VA only recognizes “hearing loss” as an official symptom.

The Claims Attributes API takes this free text and uses it to identify information that can speed up claims processing in three primary ways:

### Identifying Classification

The step of translating “ringing in my ears” into “hearing loss” is required before a claim can be established and assessed, and this translation can cause a delay. The Claims Attributes API uses a machine learning model, trained on previous, completed, anonymized claims data, to help in avoiding this delay by automatically translating between these informal free-text descriptions and their formal classifications.

### Identifying Special Issues and Flashes

Depending on the facts of the constituent contentions or information about the claimant, the claim may require a particular regional office or specialist to review it - for instance, only certain regional offices process for Agent Orange exposure. Our data has shown that when claims have flashes and special issues added early on in the lifecycle of a claim, they are processed more quickly, as they are able to be prioritized appropriately and sent to the correct regional office or specialist trained in handling them.

We can use this same claims text, in conjunction with another machine learning model, to identify these facts about the particular contentions that make up the claim (“special issues”) and the claimant who is filing (“flashes”), again speeding up processing.

### Centralizing Information

One additional benefit of this API is centralizing the models that are used to provide these classifications. Previously, individual mail vendors had copies of an in-development machine learning model that performed the above-mentioned classifications, and deployed this locally. In vending this model via a single, centrally-hosted RESTful API, we gain the ability to update and improve the model over time in a way that all parties benefit.

## Technical Overview

### Inputs and outputs

The Claims Attributes takes as input a JSON payload object with a single member entitled `claim_text`, which is an array of free-text values. One example source of this data is each row of the `Current Disability(ies)` field of section IV (“Claim Information”) from the 21-526EZ form.

It passes each item in this array one at a time through a machine learning model that has been trained on millions of previously-completed disability claims, and then outputs an object with a single `contentions` property that maps to an array with an entry for each inputted contention.

Each entry in this array contains:

- The original text

- An array of flashes identified based on this claim text

- An array of special issues identified based on this claim text

- The classification that our model identified based on this claim text. This is further broken down by the code itself, a percentage confidence, and the text of the classification code.

Note that we do not actually write any data to any database - this API is purely informational and meant only to return data that callers can use to write to a system of record.

### Structure

Externally, the Claims Attributes API is exposed to callers as a single service, but internally, it is broken down into three sub-components:

1. Contention classification
2. Special issue identification, and
3. Flash identification

We will describe each sub-component below and where / how it gets its data.

#### Contention Classification

To establish the associated formal classification code and description, we first transform these strings into numeric vectors using a locally stored copy of a[ TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) transformation that has been trained with data from millions of previous claims. For example, let’s say we have received the following free-text contentions as input:

- Ringing in my ear
- skin condition because of homelessness

Internally the vectorizer transforms these to

- [0.2, 3.4, …, 2.3]
- [1.3, .3, …, 1.7]]

After our input text has been vectorized, our classifier is effectively mapping these numeric vectors to classifications such as the following:

- code: 3140, text: hearing loss, confidence: .97
- code: 9016, text: skin, confidence: .97

It does this using a locally stored copy of a previously trained Multi-Class Logistic Regression model to make the predictions. This model has been trained with data from past benefit claims to infer the relationship between the contention a Veteran wrote down on the form and the classification a VA employee ultimately assigned to it.

##### Notes on model performance:

Taking a look at the performance of the model at different confidence thresholds, we think that the ideal confidence threshold should be 70%. Anything from 70% and above should be assigned a classification. Setting the threshold at 70% means that 85.6% of all claims will be correctly labeled while we reduce the amount of misclassified auto-establish claims to 3.3%, leaving 11.1% of claims in need of manual revision.

#### Flash Identification

Flashes are attributes appended to a claim that are related to the claimant. The Flashes sub-component receives a given contention and determines whether one or more of flashes from the below list could potentially apply:

- Hardship
- Seriously Injured/Very Seriously Injured
- Terminally Ill
- Homeless
- Purple Heart
- POW
- Medal of Honor
- Amyotrophic Lateral Sclerosis
- Emergency Care

There are three interwoven reasons as to why we have chosen this subset:

1. There is a higher than normal sense of urgency in processing these claims -- someone going through financial hardship could be about to lose their home, for instance.
2. While many flashes are purely informational, these are the subset of flashes that require a trained reviewer to handle them.
3. Our goal is to cut down on claim processing time by focusing on those issues that require specialty knowledge to process, so that we can route them to the correct person early.

A comprehensive list of (corporate) flashes and their descriptions can be found[ here](https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000036570/Appendix-C.-Index-of-Claim-Attributes#2) (see: index of corporate flashes)

As an example, the flashes sub-component might receive the following contention from Claims Attributes API: “skin condition because of homelessness”

Based on that description, it would determine that the following special issues could potentially apply: “Homeless”

It does this by performing an [edit distance]([https://en.wikipedia.org/wiki/Edit_distance#:~:text=In computational linguistics and computer,one string into the other.)](https://en.wikipedia.org/wiki/Edit_distance#:~:text=In%20computational%20linguistics%20and%20computer,one%20string%20into%20the%20other.)) analysis between the contention and phrases known to be related to the flashes listed above. If it finds a phrase within a contention or a if it close enough to one of our known phrases (think: typos) then it adds the respective flash to it.

#### Special Issue Identification

The Special Issues sub-component receives the list of contentions, determines whether a special issue from the list below could potentially apply to the claim based on the contentions, and returns the list of special issues found.

_Note: Special Issues are attributes appended to a claim that are related to the type of claim._

List of Special Issues we look for:

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

For example, the Special Issues Service might receive the following contention text from Claims Attributes API: “p.t.s.d from gulf war”.

Based on this text, we infer that the following special issue could potentially apply: “PTSD/1”

Similarly to[ Flashes Service](https://www.notion.so/Flashes-Service-f05a4fbb5ab54e67849e966d989b6528), it does this by performing an [edit distance]([https://en.wikipedia.org/wiki/Edit_distance#:~:text=In computational linguistics and computer,one string into the other.)](https://en.wikipedia.org/wiki/Edit_distance#:~:text=In%20computational%20linguistics%20and%20computer,one%20string%20into%20the%20other.)) analysis between the contention and phrases known to be related to the flashes listed above. If it finds a phrase within a contention or a if it close enough to one of our known phrases (think typos) then it adds the respective special issue to it.

At some point in the future we may also utilize a trained machine learning model to perform special issue classification.
