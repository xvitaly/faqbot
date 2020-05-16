# List of available bot actions

## Admin actions

This actions can be executed only by bot owners and admins specified in `admins` setting of configuration file.

List of currently supported admin actions:

  * `/add KEYWORD DESCRIPTION` (private messages only) - add a new keyword `KEYWORD` to the database;
  * `/remove KEYWORD` (private messages only) - remove the keyword `KEYWORD` from the database;
  * `/edit KEYWORD NEW_DESCRIPTION` (private messages only) - change description of the keyword `KEYWORD` in the database;
  * `/alias_add KEYWORD ALIAS_NAME` (private messages only) - add a new alias `ALIAS_NAME` to existing keyword `KEYWORD`;
  * `/alias_remove ALIAS_NAME` (private messages only) - remove existing alias `ALIAS_NAME` from the database;
  * `/list` (private messages only) - list available keywords.

## User actions

List of currently supported user actions:

  * `/start` - start working with the bot;
  * `/faq KEYWORD` (private messages and supergroups) - find a keyword `KEYWORD` in the database.
