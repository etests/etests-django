<template>
  <StandardLayout>
    <v-layout justify-center>
      <v-flex xs12 lg10>
        <Login />
      </v-flex>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import Login from "@/components/Login";

export default {
  props: {
    authType: {
      required: false,
      default: null
    }
  },
  data() {
    return {
      showTab: parseInt(this.authType),
      tabs: [
        {
          id: "registerStudent",
          title: "Register as Student",
          icon: "group",
          component: "RegisterStudent"
        },
        {
          id: "registerInstitute",
          title: "Register as Institute",
          icon: "business",
          component: "RegisterInstitute"
        },
        {
          id: "login",
          title: "Login",
          icon: "mdi-key-variant",
          component: "Login"
        }
      ]
    };
  },
  components: {
    StandardLayout,
    Login
  }
};
</script>
<style></style>
