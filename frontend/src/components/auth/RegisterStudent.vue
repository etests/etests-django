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
        :counter="25"
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
      <v-select
        v-model="institute"
        :items="institutes"
        :error-messages="instituteErrors"
        :counter="25"
        label="Institute"
        @input="$v.institute.$touch()"
        @blur="$v.institute.$touch()"
      ></v-select>
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
            v-model="birth_date"
            required
            label="Date of birth"
            append-icon="event"
            v-on="on"
            @change="$v.birth_date.$touch()"
            @blur="$v.birth_date.$touch()"
          ></v-text-field>
        </template>
        <v-date-picker
          ref="picker"
          scrollable
          v-model="birth_date"
          :max="new Date().toISOString().substr(0, 10)"
          min="1980-01-01"
          @input="menu = false"
        ></v-date-picker>
      </v-menu>

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
import FlexibleCardLayout from "@/components/layouts/FlexibleCardLayout.vue";

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
    email: { required, email },
    gender: { required },
    phone: {
      required,
      numeric,
      maxLength: maxLength(15),
      minLength: minLength(8)
    },
    institute: {},
    birth_date: { required },
    password: { required, minLength: minLength(8) },
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
      state: "",
      city: "",
      email: "",
      phone: "",
      gender: "",
      birth_date: "",
      institute: null,
      checkbox: false,
      password: "",
      states: ["Uttar Pradesh", "Bihar", "West Bengal", "Delhi", "Rajasthan"],
      genders: [
        { value: "M", text: "Male" },
        { value: "F", text: "Female" },
        { value: "O", text: "Others" }
      ],
      showPassword: false,
      menu: false,
      watch: {
        menu(val) {
          val && setTimeout(() => (this.$refs.picker.activePicker = "YEAR"));
        }
      }
    };
  },

  computed: {
    institutes() {
      var list = [];
      if (this.$store.state.institutes.all.items) {
        this.$store.state.institutes.all.items.forEach(function(item) {
          list.push({ value: item.pk, text: item.user.name });
        });
      }
      return list;
    },
    checkboxErrors() {
      const errors = [];
      if (!this.$v.checkbox.$dirty) return errors;
      !this.$v.checkbox.checked && errors.push("You must agree to continue.");
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
      !this.$v.city.required && errors.push("City is required.");
      !this.$v.city.maxLength &&
        errors.push("city must be at most 25 characters long");
      return errors;
    },
    instituteErrors() {
      const errors = [];
      if (!this.$v.institute.$dirty) return errors;
      else return null;
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

  created() {
    this.$store.dispatch("institutes/getAll");
  },

  methods: {
    clear() {
      this.$v.$reset();
      this.name = "";
      this.state = "";
      this.city = "";
      this.email = "";
      this.phone = "";
      this.gender = "";
      this.birth_date = null;
      this.institute = "";
      this.checkbox = false;
      this.password = "";
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
        gender,
        institute,
        // eslint-disable-next-line camelcase
        birth_date
      } = this;
      var userData = {
        user: {
          name,
          state,
          city,
          email,
          phone,
          password,
          is_student: true
        },
        gender,
        institute,
        birth_date
      };
      const { dispatch } = this.$store;
      if (checkbox) {
        dispatch("authentication/register", userData);
      }
    }
  },
  mounted() {}
};
</script>
