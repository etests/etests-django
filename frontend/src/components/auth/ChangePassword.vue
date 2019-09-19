<template>
  <FlexibleCardLayout>
    <form class="px-5 py-5 mb-4">
      <v-text-field
        :append-icon="showOldPassword ? 'visibility' : 'visibility_off'"
        :type="showOldPassword ? 'text' : 'password'"
        name="input-10-2"
        label="Old Password"
        value=""
        class="input-group--focused"
        @click:append="showOldPassword = !showOldPassword"
      ></v-text-field>

      <v-text-field
        :append-icon="showNewPassword ? 'visibility' : 'visibility_off'"
        :rules="[passwordRules.required, passwordRules.min]"
        :type="showNewPassword ? 'text' : 'password'"
        name="input-10-2"
        label="New Password"
        hint="At least 8 characters"
        value=""
        class="input-group--focused"
        @click:append="showNewPassword = !shownewPassword"
      ></v-text-field>
      <v-btn @click="submit">Change Password</v-btn>
    </form>
  </FlexibleCardLayout>
</template>

<script>
import { validationMixin } from "vuelidate";
import FlexibleCardLayout from "@/components/layouts/FlexibleCardLayout.vue";

export default {
  mixins: [validationMixin],

  data: function() {
    return {
      showNewPassword: false,
      showOldPassword: false,
      oldPassword: "",
      newPassword: "",
      passwordRules: {
        required: value => !!value || "Required.",
        min: v => v.length >= 8 || "Min 8 characters"
      }
    };
  },

  components: {
    FlexibleCardLayout
  },

  methods: {
    submit() {
      this.$v.$touch();
    }
  }
};
</script>
