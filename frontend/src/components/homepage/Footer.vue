<template>
  <SectionLayout>
    <v-layout row wrap justify-center slot="content">
      <v-flex xs12 md4>
        <v-card :class="$style.card">
          <v-layout align-center justify-center column>
            <v-flex xs12>
              <v-img
                :src="require('@/assets/images/footer/social.png')"
                width="90"
                class="mx-auto"
                :class="$style.sticker"
              />
            </v-flex>
            <v-flex xs12>
              <h3>Our Network</h3>
            </v-flex>
            <v-flex xs12 :class="['mx-5 mt-5', $style.text]">
              <p>
                eTests is the new standard in online testing solutions. We are
                in touch with over 100 institutes and thousands of students all
                over India and this number is growing very rapidly. We support
                testing for all major exams.
              </p>
            </v-flex>
            <v-flex xs12>
              <v-btn
                v-for="icon in icons"
                :key="icon.icon"
                color="primary"
                icon
                large
                :href="icon.link"
                target="blank"
              >
                <v-icon size="20px">{{ icon.icon }}</v-icon>
              </v-btn>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
      <v-flex xs12 md4>
        <v-card :class="$style.card">
          <v-layout align-center justify-center column>
            <v-flex xs12>
              <v-img
                :src="require('@/assets/images/footer/contact.png')"
                width="90"
                class="mx-auto"
                :class="$style.sticker"
              />
            </v-flex>
            <v-flex xs12>
              <h3>Contact Us</h3>
            </v-flex>
            <v-flex xs12 :class="['mx-5 my-5', $style.text]">
              <v-icon color="primary">mdi-phone-outline</v-icon><br />
              +91 78 2298 6293
              <br /><br />
              <v-icon color="primary">mdi-email-outline</v-icon> <br />
              <a href="mailto:etests.service@gmail.com">
                etests.service@gmail.com
              </a>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
      <v-flex xs12 md4>
        <v-card :class="$style.card">
          <v-layout align-center justify-center column>
            <v-flex xs12>
              <v-img
                :src="require('@/assets/images/footer/links.png')"
                width="90"
                class="mx-auto"
                :class="$style.sticker"
              />
            </v-flex>
            <v-flex xs12>
              <h3>Important Links</h3>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
  </SectionLayout>
</template>

<script>
import SectionLayout from "@/components/homepage/SectionLayout.vue";

export default {
  props: {
    authType: {
      required: false,
      default: 0
    }
  },
  data() {
    return {
      icons: [
        {
          icon: "mdi-facebook",
          link: "https://www.facebook.com/etests.india/"
        },
        { icon: "mdi-twitter", link: "https://twitter.com/eTestsIndia" },
        {
          icon: "mdi-linkedin",
          link: "https://www.linkedin.com/company/etestservice"
        },
        { icon: "mdi-instagram", link: "" }
      ]
    };
  },
  components: {
    SectionLayout
  }
};
</script>

<style module lang="stylus">
.card{
   margin: 25px 40px;
   border-radius: 15px;
   max-width: 98%;
   height: 90%;
   padding: 10px 20px;

   .sticker{
     position: relative;
     top: -50px;
   }

   h3{
     font-family: "Product Sans Thin";
     font-size: 18pt;
   }
   .text{
     font-family: "Product Sans Light";
     font-size: 12pt;
     p{
      text-align: justify;
     }
   }
}
</style>
