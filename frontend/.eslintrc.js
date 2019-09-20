module.exports = {
  "root": true,
  parserOptions: {
    parser: 'babel-eslint'
  },
  "extends": [
    "plugin:vue/essential",
    "plugin:prettier/recommended",
    "eslint:recommended"
  ],
  rules: {
    "no-unused-vars": "off",
    "no-undef": "off"
  }
}
