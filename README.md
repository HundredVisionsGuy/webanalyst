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
* Fix test_clerk to work with browser from fixture
* Find a way to hide tests for clerk and other similar packages from production (we only need ones for the project)
  * I'm thinking we need to separate the files and their tests into their own repos.
* Set up the tests so that with a flag in the command, we run all tests on project folder (not tests/test_files/project)
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
    * if HTML has CSS
      * note the file name
      * run the code through the CSS validator
        + if it has errors, save error report
      * mark the file and whether it had errors or not
5. Check each CSS file for validity
6. Compile and send report
### Notes on regex expressions (for stylesheet_analyst.py)
For a sample of the regex expressions I'm using, try https://regex101.com/r/5uaYPq/1

***TODO***
### Pre-assessment
The goal of the pre-assessment is for students to attempt to demonstrate as many of the skills from the post-test as possible

### 1-page HTML document
Students will be asessed on the following traits

### Post-assessment
Students will be given an open-ended web project that will contain all the tests as the pre-assessment to demonstrate what all students have learned

## Student Proficiency Ranking (levels)
### 101 (Entry Level)
#### HTML
At this level, students are just getting started. They can make single web pages, albeit with some errors. 
Elements that students should be proficient at before moving on are as follows:
* headers
* paragraphs
* style
* links
* images
#### CSS
Students at this level only need to demonstrate basic CSS syntax and adjusting colors, background colors, and fonts (at a minimum a font applied to body (or html)). In addition, color and background color must be applied to body or html and meet color contrast analyzer

----------

### 201 (Junior Level)
#### HTML
At this level, students are able to work with lists, basic tables, and applying proper nesting and demonstrate an understanding of block versus inline tags. They should also know the difference between an ID and a CLASS attribute.
Necessary tags for demonstration of mastery (in addition to the ones listed above) are:
* table, tr, td
* ul, ol, li
* figure, figcaption
* strong, em
* div, span
#### CSS
At this point, students should be able to target elements by class and id. They should also be able to demonstrate control of the box model, floats, and possibly layouts (like setting the width and centering a page).

Students should also be able to target multiple tags with one declaration block as well as target tags inside of other tags.

----------

### 301 (Intermediate Level)
#### HTML
At this point, students need to be able to create a variety of web layouts that include a navbar mockup (or actual working navbar).

No HTML documents should be using style tags, but instead should be linking to external CSS files.

Students should also be able to use advanced table tags and attributes (such as thead, tbody, colspan, and rowspan).

Students should also be able to structure their pages using the HTML structure tags such as article, header, footer, aside, and section.

#### CSS
At this stage, students should be able to create layouts using CSS properties such as flex display, inline-block, and possibly the grid.

Students should also be applying solid design skills such as use of negative space, effective color palettes, typography.

----------

### 401 (Senior Level)
#### HTML
At this level, students should be comfortable creating full-blown websites that employ multiple pages that all link to the same style-sheet/s and use a consistent nav-bar. 

Students should be able to demonstrate the markup belonging to forms as well as form validation.

They should be able to showcase their skills through a portfolio of work or a web project (like a company site or travel brochure or web app). 

#### CSS
At this point, students should be continuing to develop their layout and design skills. They should also begin to apply a mobile-first, responsive design technique.

They should be able to design a home page that makes use of a variety of columns (single, 2-column, 3 column) using visual elements like cards, pull-quotes, and subtle animations.