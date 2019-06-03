<template>
  <FlexibleCardLayout>
    <form class="px-5 py-5 mb-4">
      <v-text-field
        v-model="name"
        :error-messages="nameErrors"
        :counter="25"
        label="Name"
        required
        @input="$v.name.$touch()"
        @blur="$v.name.$touch()"
      ></v-text-field>
      <v-select
        v-model="state"
        :items="states"
        :error-messages="stateErrors"
        label="State"
        required
        @change="$v.state.$touch()"
        @blur="$v.state.$touch()"
      ></v-select>
      <v-text-field
        v-model="city"
        :error-messages="cityErrors"
        :counter="25"
        label="City"
        required
        @input="$v.city.$touch()"
        @blur="$v.city.$touch()"
      ></v-text-field>
      <v-text-field
        v-model="email"
        :error-messages="emailErrors"
        label="E-mail"
        required
        @input="$v.email.$touch()"
        @blur="$v.email.$touch()"
      ></v-text-field>
      <v-text-field
        v-model="phone"
        :error-messages="phoneErrors"
        label="Mobile"
        required
        @input="$v.phone.$touch()"
        @blur="$v.phone.$touch()"
      ></v-text-field>
      <v-text-field
        v-model="pincode"
        :error-messages="pincodeErrors"
        label="Pincode"
        required
        @input="$v.phone.$touch()"
        @blur="$v.phone.$touch()"
      ></v-text-field>

      <v-text-field
        :append-icon="showPassword ? 'visibility' : 'visibility_off'"
        :error-messages="passwordErrors"
        required
        v-model="password"
        @input="$v.password.$touch()"
        @blur="$v.password.$touch()"
        :type="showPassword ? 'text' : 'password'"
        label="Password"
        hint="At least 8 characters"
        value=""
        class="input-group--focused"
        @click:append="showPassword = !showPassword"
      ></v-text-field>

      <v-checkbox
        v-model="checkbox"
        :error-messages="checkboxErrors"
        label="Do you agree?"
        required
        @change="$v.checkbox.$touch()"
        @blur="$v.checkbox.$touch()"
      ></v-checkbox>
      <v-btn @click="handleSubmit">submit</v-btn>
      <v-btn @click="clear">clear</v-btn>
    </form>
  </FlexibleCardLayout>
</template>

<script>
import { validationMixin } from "vuelidate";
import FlexibleCardLayout from "@components/layouts/FlexibleCardLayout.vue";

import {
  required,
  maxLength,
  email,
  numeric,
  minLength
} from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    name: { required, maxLength: maxLength(25) },
    state: { required, maxLength: maxLength(25) },
    city: { required, maxLength: maxLength(25) },
    pincode: { required, maxLength: maxLength(8) },
    email: { required, email },
    phone: {
      required,
      numeric,
      maxLength: maxLength(15),
      minLength: minLength(8)
    },
    password: { required, minLength: minLength(8) },
    checkbox: {
      checked(val) {
        return val;
      }
    }
  },

  data: function() {
    return {
      name: "",
      email: "",
      phone: "",
      state: "",
      city: "",
      pincode: "",
      password: "",
      checkbox: false,
      states: ["Uttar Pradesh", "Bihar", "West Bengal", "Delhi", "Rajasthan"],
      showPassword: false
    };
  },

  components: {
    FlexibleCardLayout
  },

  computed: {
    checkboxErrors() {
      const errors = [];
      if (!this.$v.checkbox.$dirty) return errors;
      !this.$v.checkbox.checked && errors.push("You must agree to continue!");
      return errors;
    },
    nameErrors() {
      const errors = [];
      if (!this.$v.name.$dirty) return errors;
      !this.$v.name.maxLength &&
        errors.push("Name must be at most 25 characters long");
      !this.$v.name.required && errors.push("Name is required.");
      return errors;
    },
    stateErrors() {
      const errors = [];
      if (!this.$v.state.$dirty) return errors;
      !this.$v.state.required && errors.push("State is required.");
      !this.$v.state.maxLength &&
        errors.push("State must be at most 25 characters long");
      return errors;
    },
    cityErrors() {
      const errors = [];
      if (!this.$v.city.$dirty) return errors;
      !this.$v.city.required && errors.push("city is required.");
      !this.$v.city.maxLength &&
        errors.push("city must be at most 25 characters long");
      return errors;
    },
    pincodeErrors() {
      const errors = [];
      if (!this.$v.pincode.$dirty) return errors;
      !this.$v.pincode.required && errors.push("Pin is required.");
      !this.$v.pincode.maxLength &&
        errors.push("city must be at most 8 characters long");
      return errors;
    },
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Must be valid e-mail");
      !this.$v.email.required && errors.push("E-mail is required");
      return errors;
    },
    phoneErrors() {
      const errors = [];
      if (!this.$v.phone.$dirty) return errors;
      !this.$v.phone.required && errors.push("Mobile Number is required");
      !this.$v.phone.numeric &&
        errors.push("Phone Number must be entirely numeric");
      !this.$v.phone.minLength && errors.push("Must be at least 8 digits");
      !this.$v.phone.maxLength && errors.push("Must be at most 15 digits");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.minLength &&
        errors.push("Password must be at least 8 characters long.");
      !this.$v.password.required && errors.push("Password is required.");
      return errors;
    }
  },

  methods: {
    clear() {
      this.$v.$reset();
      this.name = "";
      this.state = "";
      this.city = "";
      this.pincode = "";
      this.email = "";
      this.phone = "";
      this.password = "";
      this.checkbox = false;
    },
    handleSubmit(e) {
      this.$v.$touch();
      this.submitted = true;
      const {
        name,
        state,
        city,
        email,
        phone,
        checkbox,
        password,
        pincode
      } = this;
      var userData = {
        user: {
          name,
          state,
          city,
          email,
          phone,
          password,
          is_institute: true
        },
        pincode
      };
      console.log(JSON.stringify(userData));
      const { dispatch } = this.$store;
      if (checkbox) {
        dispatch("authentication/register", userData);
      }
    }
  },
  mounted() {}
};
</script>
