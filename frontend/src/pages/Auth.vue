<template>
  <v-container>
    <Header :showDrawer="false" :temporaryDrawer="true">
      <v-tabs slot="tabs" v-model="showTab" color="transparent" centered>
        <v-tabs-slider color="white"></v-tabs-slider>
        <v-tab v-for="(tab, i) in tabs" :key="i">
          <v-icon>{{ tab.icon }}</v-icon>
          &nbsp;
          <strong>{{ tab.title }}</strong>
        </v-tab>
      </v-tabs>
    </Header>
    <v-content>
      <v-layout row>
        <v-flex xs12>
          <v-tabs-items v-model="showTab">
            <v-tab-item v-for="(tab, i) in tabs" :key="i">
              <component :is="tab.component" />
            </v-tab-item>
          </v-tabs-items>
        </v-flex>
      </v-layout>
      <Footer :fixed="true" />
    </v-content>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";
import RegisterStudent from "../components/auth/RegisterStudent";
import RegisterInstitute from "../components/auth/RegisterInstitute";
import Login from "../components/auth/Login";
import ForgotPassword from "../components/auth/ForgotPassword";
import ChangePassword from "../components/auth/ChangePassword";

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
    Header,
    RegisterStudent,
    RegisterInstitute,
    Login,
    ForgotPassword,
    ChangePassword,
    Footer
  }
};
</script>
<style></style>
