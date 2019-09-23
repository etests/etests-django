module.exports = {
  root: true,
  parserOptions: {
    parser: 'babel-eslint'
  },
  env: {
    browser: true,
  },
  extends: [
    'plugin:vue/essential',
    "plugin:prettier/recommended",
    'plugin:prettier/recommended',
  ],
  plugins: [
    'vue'
  ],
  rules: {
    "no-unused-vars": "off",
    "no-undef": "off",
    'generator-star-spacing': 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off'
  }
}
