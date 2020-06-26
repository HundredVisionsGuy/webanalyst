# Web Analyst
This project is designed to assess students' ability to code clean, semantic front-end technologies (HTML, CSS, JavaScript) for a variety of open-ended tasks and projects.

When selecting skills and practices, we will be using the [Mozilla Developer Network](https://developer.mozilla.org/) as the final arbiter of styles and best practices. 

## Important Notes
* Until we have a folder structure selected and a license, we will not be accepting pull requests

## Project Structure & Architecture
Python® is used as the scripting language for performing tests and reports.
We are still selecting license and folder structure.

### Git branching / release model
For this project, we'll be using the git branching model from [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) by Vincent Driessen

## TODO
* Create a report format to report back findings from a project
* Identify what errors the HTML validator does NOT catch
* Identify how to catch those errors through AdvancedHTMLParser

## Structure
This project will be structured by levels and concepts.
There will be a test file for each concept and level:
* a test for errors in HTML and CSS (using the validator)
* one test file for HTML for each level of "proficiency"
* One test file for each level of tables (one for simple table)
* a test for lists at two levels
* a test for links 
* a test for images
* a set of tests for multiple files
  * is there an index file name or not?
  * are the HTML files linking to at least one CSS file?
  * etc.
* and so on...

## Skills Assessed / Unit Tests
*Syntax*
Some of the things I will be testing for is:

HTML:
  * all element and attribute names are lowercase
  * all attribute values are in double quotes
  * no attributes in closing tags
  * all ID attribute names are unique on a page
  * all multi-word attribute values use hypen-case (or dash-case)

CSS:
  * no inline styles
  * in CSS use expanded syntax
  * See [Use expanded syntax](https://developer.mozilla.org/en-US/docs/MDN/Contribute/Guidelines/Code_guidelines/CSS#Use_expanded_syntax) example 
      - include a space between selector and opening curley brace 
      - Always include a semi-colon at the end of the last declaration, even though it isn't strictly necessary.
      - Put the closing curly brace on a new line.
      -In each declaration, put a space after the separating colon, but not before.
      - NOTE: we opted to leave out indentation guidelines
    * use double quotes for all values
    * Function parameters should have spaces after their separating commas, but not before
    * Don't use `@import`
    * When turning off properties, always use a `0` over `none`
    * Don't repeat the exact same selectors
      - unless in separate `@media` queries
    * Always apply all general styles before `@media` queries
    * Apply a mobile-first approach to CSS
      - use only `min-width` for your `@media` queries
      - always have the `min-width` values increase in size as you move down the stylesheet

*Semantics*
For semantics, I will be looking at the following:
  * The `<head>` and `<body>` elements are nested inside of the `<html>` element
  * `<title>` element is inside the `<head>`
  * All `<body>` elements are nested inside the `<body>` element
  * The page contains only one `<h1>` element

*Validation*
  * uses HTML5 doctype
  * lang attribute is set
  * charset is set to utf-8
  * includes viewport meta tag

From [HTML guidelines](https://developer.mozilla.org/en-US/docs/MDN/Contribute/Guidelines/Code_guidelines)
and [CSS guidelines](https://developer.mozilla.org/en-US/docs/MDN/Contribute/Guidelines/Code_guidelines/)

## Student Tasks
Students will be given a pre-test, a series of tasks to complete that will progress through the skills.

## Analyzer Tasks
1. create a list of all HTML & CSS files from project folder
2. Check each HTML file for validity
3. Check each HTML file for other tests
4. Check each HTML file for CSS code
  - if HTML has CSS
    * note the file name
    * run the code through the CSS validator
      + if it has errors, save error report
    * mark the file and whether it had errors or not
5. Check each CSS file for validity
6. Compile and send report

***TODO***
### Pre-assessment
The goal of the pre-assessment is for students to attempt to demonstrate as many of the skills from the post-test as possible

### 1-page HTML document
Students will be asessed on the following traits

### Post-assessment
Students will be given an open-ended web project that will contain all the tests as the pre-assessment to demonstrate what all students have learned