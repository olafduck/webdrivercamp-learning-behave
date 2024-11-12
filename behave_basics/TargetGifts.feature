Feature: Target Gifts

  Background:
    Given Navigate to https://www.target.com/

  Scenario: Navigate to the page
    When Search for Gift Ideas

  Scenario Outline: Verify searched page's headers
    When Search for <search_item>
    Then Verify header of the page contains <search_item>

    Examples:
      | search_item |
      | Gift Ideas  |
      | iPhone      |

  Scenario: Gifts - Price validation
    When Search for Gift Ideas
    When Select Her in Who are you shopping for? section
    When Select Gifts under $15 in Great gifts for any budget section
    Then Collect all items on the first page into collected_items
    Then Verify all collected results' price is < 15
      | context.collected_items |
