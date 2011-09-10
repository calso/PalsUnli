Feature: Account related features

	Scenario: Account Index
		When I access the url "/accounts/"
		Then I see the header "Account Dashboard"

	Scenario: Account Login
		When I access the url "/accounts/login/"
		Then I see the header "Login"
		Given a user "anna" with password "1234"
		Then login as "anna" with password "1234"

	Scenario: Account Edit
		Given a user "anna" with password "1234" and
		When I login as "anna" with password "1234"
		And I access the url "/accounts/edit/"
		Then I see the header "Edit Profile"
