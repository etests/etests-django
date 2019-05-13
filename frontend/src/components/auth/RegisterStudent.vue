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
        :error-messages="statesErrors"
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
      <v-select
        v-model="gender"
        :items="genders"
        :error-messages="genderErrors"
        label="Gender"
        required
        @change="$v.gender.$touch()"
        @blur="$v.gender.$touch()"
      ></v-select>
      <v-text-field
        v-model="coaching"
        :error-messages="coachingErrors"
        :counter="25"
        label="Institute"
        @input="$v.coaching.$touch()"
        @blur="$v.coaching.$touch()"
      ></v-text-field>
      <v-menu
        ref="menu"
        v-model="menu"
        :close-on-content-click="false"
        :nudge-right="40"
        lazy
        transition="scale-transition"
        offset-y
        full-width
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            v-model="date"
            label="Date of birth"
            prepend-icon="event"
            readonly
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          ref="picker"
          v-model="date"
          :max="new Date().toISOString().substr(0, 10)"
          min="1950-01-01"
          @change="save"
        ></v-date-picker>
      </v-menu>

      <v-text-field
        :append-icon="showPassword ? 'visibility' : 'visibility_off'"
        :rules="[passwordRules.required, passwordRules.min]"
        :type="showPassword ? 'text' : 'password'"
        name="input-10-2"
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
      <v-btn @click="submit">submit</v-btn>
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
    city: { required, maxLength: maxLength(25) },
    email: { required, email },
    gender: { required },
    state: { required },
    phone: {
      required,
      numeric,
      maxLength: maxLength(15),
      minLength: minLength(8)
    },
    coaching: { maxLength: maxLength(50) },
    checkbox: {
      checked(val) {
        return val;
      }
    }
  },

  components: {
    FlexibleCardLayout
  },

  data: function() {
    return {
      name: "",
      email: "",
      phone: "",
      city: "",
      gender: null,
      state: null,
      states: ["A", "B", "C"],
      coaching: "",
      genders: ["Male", "Female", "Others"],
      showPassword: false,
      password: "",
      passwordRules: {
        required: value => !!value || "Required.",
        min: v => v.length >= 8 || "Min 8 characters"
      },
      date: null,
      menu: false,
      watch: {
        menu(val) {
          val && setTimeout(() => (this.$refs.picker.activePicker = "YEAR"));
        }
      },
      checkbox: false
    };
  },

  computed: {
    checkboxErrors() {
      const errors = [];
      if (!this.$v.checkbox.$dirty) return errors;
      !this.$v.checkbox.checked && errors.push("You must agree to continue!");
      return errors;
    },
    genderErrors() {
      const errors = [];
      if (!this.$v.gender.$dirty) return errors;
      !this.$v.gender.required && errors.push("Gender is required");
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
    cityErrors() {
      const errors = [];
      if (!this.$v.city.$dirty) return errors;
      !this.$v.city.maxLength &&
        errors.push("city must be at most 25 characters long");
      !this.$v.city.required && errors.push("city is required.");
      return errors;
    },
    coachingErrors() {
      const errors = [];
      if (!this.$v.coaching.$dirty) return errors;
      !this.$v.coaching.maxLength &&
        errors.push("Name must be at most 25 characters long");
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
    }
  },

  methods: {
    submit() {
      this.$v.$touch();
    },
    clear() {
      this.$v.$reset();
      this.name = "";
      this.city = "";
      this.email = "";
      this.phone = "";
      this.gender = null;
      this.date = null;
      this.coaching = "";
      this.checkbox = false;
      this.password = "";
    }
  },
  save(date) {
    this.$refs.menu.save(date);
  },
  mounted() {}
};
</script>
