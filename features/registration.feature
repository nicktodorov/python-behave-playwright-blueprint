Feature: Registration Step 1
  As a user, I want to complete the first step of registration so I can receive an activation code.

  @positive
  Scenario: Successful registration step one triggers activation popup
    Given I am on login page
    And I navigate to the registration page
    When I fill in the registration details with a valid email and password
    And I accept the terms and conditions
    And I click the Register button
    Then the activation code popup should be displayed

  @negative
  Scenario Outline: Registration fails with invalid credentials or missing consent
    Given I am on login page
    And I navigate to the registration page
    When I fill in the registration details with "<email>" and "<password>"
    And I set the terms and conditions checkbox to "<terms_state>"
    And I click the Register button
    Then the registration should be blocked due to "<error_reason>"

    Examples:
      | email             | password       | terms_state | error_reason                       |
      | invalid_email.com | SecurePass123! | checked     | Invalid e-mail                     |
      | [DYNAMIC]         | 12             | checked     | Password too short                 |
      | [DYNAMIC]         | SecurePass123! | unchecked   | Required field                     |
      | [BLANK]           | SecurePass123! | checked     | Required field                     |
      | [DYNAMIC]         | [BLANK]        | checked     | Required field                     |
      | valid@example.com | SecurePass123! | checked     | User with this email already exist |
