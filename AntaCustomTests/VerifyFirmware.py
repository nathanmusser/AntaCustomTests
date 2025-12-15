from anta.models import AntaTest, AntaCommand, AntaTemplate, ClassVar
from anta.decorators import skip_on_platforms


class VerifyFN0094 (AntaTest):
    """Verifies 7280R3 patched for Field Notice 0094.

    Expected Results
    ----------------
    * Success: The test will pass if the device is running the minimum firmware version of 6 or greater.
    * Failure: The test will fail if the device is running less than the minimum firmware version of 6.

    Examples
    --------
    ```yaml
    verifyFirmware:
      - VerifyFN0094:
    ```
    """

    categories: ClassVar[list[str]] = ["software"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show version detail", revision=1)]


    @skip_on_platforms(["cEOSLab", "vEOS-lab", "cEOSCloudLab"])
    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyFN0094."""
        command_output = self.instance_commands[0].json_output
        affected_models_a = [
            "DCS-7280SR3K-48YC8-F",
            "DCS-7280SR3K-48YC8-R",
            "DCS-7280SR3-48YC8-R",
            "DCS-7280SR3-48YC8-F", 
            "DCS-7280SR3K-48YC8A-R", 
            "DCS-7280SR3K-48YC8A-F",
        ]
        affected_models_b = [
            "DCS-7280SR3M-48YC8-F", 
            "DCS-7280SR3M-48YC8-R", 
            "DCS-7280SR3MK-48YC8A-S-F",
            "DCS-7280SR3MK-48YC8A-S-R",
        ]
        minimum_version = 6
        if any(model in command_output["modelName"] for model in affected_models_a):
            self.result.is_success()
            if int(float(command_output["FixedSystemvrm2"])) < minimum_version:
                self.result.is_failure(f"Firmware version below minimum - Actual: {command_output['imageFormatVersion']} Minimum: {minimum_version}")
        elif any(model in command_output["modelName"] for model in affected_models_b):
            self.result.is_success()
            if int(float(command_output["FixedSystemvrm4"])) < minimum_version:
                self.result.is_failure(f"Firmware version below minimum - Actual: {command_output['imageFormatVersion']} Minimum: {minimum_version}")
        else:
            self.result.is_skipped("Not affected model")
