# Security

The API gateway security requirements are documented [here](https://community.max.gov/pages/viewpage.action?pageId=2138665329) (VA-Internal Only).

Code in this repository must undergo both a Fortify static code analysis and a WASA penetration test.

## Fortify Static Code Analysis

General Fortify instructions are present on the Fortify scan wiki [here](https://teams.microsoft.com/l/team/19%3a59d9ecebfcc948ecb3a67e3f7e15cec9%40thread.skype/conversations?groupId=3c2ed08f-9317-46fc-9d9a-5d7b71d1816f&tenantId=e95f1b23-abaf-45ee-821d-b7ab251ab3bf) (VA Internal Only).

To scan this repository, in order to ensure you have installed all dependencies, it is necessary to gather the requirements for each microservice together, install into a single virtual environment, and include this virtual environment in the `-python-path` argument to the Fortify script.

You can run the `Fortify Scan Wizard` to generate a new scan, or, if you're on Linux/MacOS, you can run the existing `Fortifyclaims-attributes-api.sh`.

This is all done for you in the `security-scan` Makefile target:

1. Download the above linked-to executable, license, and rule packs
2. Put `Fortify_SCA_and_Apps_x.y.z/bin` into your `PATH`
3. Run the scan from the top-level of this repository with:
   ```sh
   make security-scan
   ```

## WASA Scan

Following the passing of the Fortify static scan, it is necessary to run a WASA scan. You can find instructions for this [here](https://community.max.gov/display/VAExternal/Requesting+a+WASA+Assessment) (VA Internal only).
