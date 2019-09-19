<template>
  <SectionLayout>
    <template slot="heading">
      Subscribe Now!
    </template>
    <template slot="subheading">
      Keep yourself updated about our latest features
    </template>
    <v-layout slot="content" mt-5 justify-center>
      <v-flex xs10 md8 lg6>
        <v-form v-model="valid">
          <v-text-field
            v-model="name"
            :rules="nameRules"
            label="Name"
            outline
            required
          ></v-text-field>
          <v-text-field
            v-model="email"
            :rules="emailRules"
            label="E-mail"
            outline
            required
          ></v-text-field>
          <v-btn round large dark color="primary">
            Subscribe
          </v-btn>
        </v-form>
      </v-flex>
    </v-layout>
  </SectionLayout>
</template>

<script>
import SectionLayout from "@/components/homepage/SectionLayout.vue";

export default {
  name: "subscribe",
  data() {
    return {
      valid: false,
      name: "",
      nameRules: [
        v => v.length <= 10 || "Name must be less than 10 characters"
      ],
      email: "",
      emailRules: [v => /.+@.+/.test(v) || "E-mail must be valid"]
    };
  },
  components: {
    SectionLayout
  }
};
</script>
