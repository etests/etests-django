<template>
  <v-tabs centered color="cyan" dark icons-and-text>
    <v-tabs-slider color="yellow"></v-tabs-slider>

    <v-tab href="#tab-1">
      Student Registration
      <v-icon>group</v-icon>
    </v-tab>

    <v-tab href="#tab-2">
      Institute Registration
      <v-icon>business</v-icon>
    </v-tab>

    <v-tab href="#tab-3">
      Login
      <v-icon>input</v-icon>
    </v-tab>

    <v-tab-item :value="'tab-' + 1">
      <v-card flat>
        <Registerstudent />
      </v-card>
    </v-tab-item>

    <v-tab-item :value="'tab-' + 2">
      <v-card flat>
        <Registercoaching />
      </v-card>
    </v-tab-item>

    <v-tab-item :value="'tab-' + 3">
      <v-card flat>
        <Login />
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>
<!-- <v-layout>
    
    
    <Forgot />
    <Change />
    
  </v-layout> -->
<script>
import Registerstudent from "../components/auth/Registerstudent";
import Registercoaching from "../components/auth/Registercoaching";
import Login from "../components/auth/Login";
import Forgot from "../components/auth/Forgot";
import Change from "../components/auth/Changepassword";

export default {
  components: {
    Registerstudent,
    Registercoaching,
    Login,
    Forgot,
    Change
  }
};
</script>
<style></style>
