Feature: Phone related features

	Scenario: Phone Index
	    When I access the url "/phone/"
	    Then I see the header "Phone Dashboard"
	    And I see "Add" link
