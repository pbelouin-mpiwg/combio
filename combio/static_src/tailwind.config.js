/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
  content: [
    /**
     * HTML. Paths to Django template files that will contain Tailwind CSS classes.
     */

    /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    "../templates/**/*.html",

    /*
     * Main templates directory of the project (BASE_DIR/templates).
     * Adjust the following line to match your project structure.
     */
    "../../templates/**/*.html",

    /*
     * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
     * Adjust the following line to match your project structure.
     */
    "../../**/templates/**/*.html",

    /**
     * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
     * patterns match your project structure.
     */
    /* JS 1: Ignore any JavaScript in node_modules folder. */
    // '!../../**/node_modules',
    /* JS 2: Process all JavaScript files in the project. */
    // '../../**/*.js',

    /**
     * Python: If you use Tailwind CSS classes in Python, uncomment the following line
     * and make sure the pattern below matches your project structure.
     */
    // '../../**/*.py'
  ],
  safelist: ["bg-mpiwg-subdued-green"],
  theme: {
    fontFamily: {
      sans: [
        '"Open Sans"',
        "Calibri",
        '"Helvetica Now"',
        "Helvetica",
        "Roboto",
        "Arial",
      ],
      serif: ['"Sectra Book"', "Times", "Vollkorn"],
      mpiwg: ['"Apercu Pro"'],
    },
    extend: {
      colors: {
        "mpiwg-green": "#006464",
        "mpiwg-subdued-green": "#739187",
        "mpiwg-light-green": "#50FA96",
        "mpiwg-brown": "#C3BEB9",
        "mpiwg-blue": "#d5dbdf",
        "mpiwg-yellow": "#ece7cf",
        "mpiwg-light-brown": "#fbfafa",
        "mpiwg-beige": "#e1e1dc",
        "vintage-salmon": "#FEF8EE",
        "error-red": "#fccccc",
        "dark-red": "#660e0e",
        "nice-gray": "#d5d8de",
        "light-charcoal": "#545454",
        charcoal: "#333",
        "dark-charcoal": "#414141",
        "lighter-charcoal": "#a0a0a0",
        "middle-charcoal": "#727272",
        "fancy-grey": "#dddddd",
        "dis-charcoal": "8a8a8a",
      },
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
