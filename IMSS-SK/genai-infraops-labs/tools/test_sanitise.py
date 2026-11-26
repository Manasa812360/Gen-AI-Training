import pytest

from tools.sanitise import sanitise


@pytest.mark.parametrize(
    ("category", "value"),
    [
        ("INDIAN_MOBILE", "+91 98220 12345"),
        ("INDIAN_MOBILE", "9876543210"),
        ("INDIAN_MOBILE", "+91-90110-55667"),
        ("EMPLOYEE_ID", "HM-482913"),
        ("AWS_ACCESS_KEY", "AKIAIOSFODNN7EXAMPLE"),
        ("AWS_SECRET_KEY", "secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"),
        (
            "BEARER_TOKEN",
            "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0In0.abc123def456",
        ),
        ("JWT_TOKEN", "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0In0.abc123def456"),
        ("UNC_PATH", r"\\fs-pune-01\finance\payroll"),
        ("CONNECTION_STRING_PASSWORD", "Password=Fin@pp#2026"),
    ],
)
def test_sanitise_masks_named_sensitive_values(category, value):
    mapping = {}

    clean, found = sanitise(f"Value: {value}", mapping)

    assert clean == f"Value: <{category}_1>"
    assert found == [category]


def test_sanitise_uses_stable_tokens_within_a_record():
    clean, found = sanitise("HM-482913 and HM-482913, but not HM-48291", {})

    assert clean == "<EMPLOYEE_ID_1> and <EMPLOYEE_ID_1>, but not HM-48291"
    assert found == ["EMPLOYEE_ID", "EMPLOYEE_ID"]


@pytest.mark.parametrize("value", ["1234567890", "51234567890", "+91 1234567890"])
def test_sanitise_preserves_non_indian_mobile_numbers(value):
    clean, found = sanitise(value, {})

    assert clean == value
    assert "INDIAN_MOBILE" not in found


@pytest.mark.parametrize(
    "value",
    [
        "AWS_SECRET_ACCESS_KEY=" + "A" * 39 + "/",
        'aws_secret_access_key="' + "A" * 39 + '="',
        "secret access key: " + "A" * 40,
    ],
)
def test_sanitise_masks_labelled_aws_secret_assignments(value):
    clean, found = sanitise(value, {})

    assert clean == "<AWS_SECRET_KEY_1>"
    assert found == ["AWS_SECRET_KEY"]


def test_sanitise_masks_unc_path_with_ip_server_as_one_value():
    clean, found = sanitise(r"\\10.20.14.22\share\file.txt", {})

    assert clean == "<UNC_PATH_1>"
    assert found == ["UNC_PATH"]


def test_sanitise_masks_jwt_with_non_word_signature_end():
    clean, found = sanitise("eyJhbGci.test.signature-", {})

    assert clean == "<JWT_TOKEN_1>"
    assert found == ["JWT_TOKEN"]


@pytest.mark.parametrize("password", ['Password="value; with spaces"', "pwd='value; with spaces'"])
def test_sanitise_masks_quoted_connection_string_password(password):
    clean, found = sanitise(f"Server=db;{password};Database=app", {})

    assert clean == "Server=db;<CONNECTION_STRING_PASSWORD_1>;Database=app"
    assert found == ["CONNECTION_STRING_PASSWORD"]
