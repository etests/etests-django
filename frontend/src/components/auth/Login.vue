<template>
  <FlexibleCardLayout>
    <form class="px-5 py-5 mb-4">
      <v-text-field
        v-model="username"
        label="Phone / Email"
        required
      ></v-text-field>
      <v-text-field
        :append-icon="showPassword ? 'visibility' : 'visibility_off'"
        :type="showPassword ? 'text' : 'password'"
        v-model="password"
        name="input-10-2"
        label="Password"
        value=""
        class="input-group--focused"
        @click:append="showPassword = !showPassword"
      ></v-text-field>
      <v-btn @click="handleSubmit">Login</v-btn>
    </form>
  </FlexibleCardLayout>
</template>

<script>
import FlexibleCardLayout from "@/components/layouts/FlexibleCardLayout.vue";

export default {
  data: function() {
    return {
      username: "",
      password: "",
      showPassword: false,
      submitted: false
    };
  },

  components: {
    FlexibleCardLayout
  },
  computed: {
    loggingIn() {
      return this.$store.state.authentication.status.loggingIn;
    }
  },
  created() {
    if (this.$store.state.authentication.status.loggedIn)
      this.$router.push({ name: "home" });
  },
  methods: {
    handleSubmit(e) {
      this.submitted = true;
      const { username, password } = this;
      const { dispatch } = this.$store;
      if (username && password) {
        dispatch("authentication/login", { username, password });
      }
    }
  }
};
</script>
