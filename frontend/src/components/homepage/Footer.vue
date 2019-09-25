<template>
  <SectionLayout>
    <v-layout row wrap justify-center slot="content">
      <v-flex xs12 md3>
        <v-card :class="$style.card" elevation="0" class="transparent">
          <v-layout align-center justify-center column>
            <v-flex xs12>
              <div :class="$style.heading">Our Network</div>
            </v-flex>
            <v-flex xs12 :class="['mx-5 mt-5', $style.text]">
              <p>
                eTests is the new standard in online testing solutions. Number
                of Institutes conducts their exams and create and sell their
                Question Banks on etests. Students from all over india preparing
                for pre-engineering and pre-medical examinations are geting
                benifit from our services.
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
      <v-flex xs12 md3>
        <v-card :class="$style.card" elevation="0" class="transparent">
          <v-layout align-center justify-center column>
            <v-flex xs12>
              <div :class="$style.heading">Contact Us</div>
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

      <v-flex xs12 md3>
        <v-card :class="$style.card" elevation="0" class="transparent">
          <v-layout align-center justify-center column>
            <v-flex xs12>
              <div :class="$style.heading">Let Us Help You</div>
              <v-list :class="['mx-5 mt-4 transparent', $style.text]">
                <strong>100% support</strong>
                <v-list-tile-content>
                  <p v-if="userType === 'student'">
                    You can practice all types of questions including Single
                    Correct, Multiple Correct, Integer Types, Matrix Match for
                    your competitive exams. After the completion of exam the
                    detailed analysis of your performance using pie charts and
                    bar graphs are generated. You can review each question and
                    responses made by you including the time you spent on each
                    question during the test. We promise to give you 100%
                    support in the services. Any technical issue raised
                    regarding exams or question banks or any payment made by you
                    will be resolved within 24 hrs.
                  </p>
                </v-list-tile-content>
                <v-list-tile-content>
                  <p v-if="userType === 'institute'">
                    Our online testing platform is developed and tested by team
                    of IITians. We have support for wide range of examination
                    pattern There is special support for
                    engineering (including JEE Main and JEE Advanced) and
                    medical (including NEET and AIIMS) entrance exams. In case of any
                    issues you can contact us and we will try our best to help.
                  </p>
                </v-list-tile-content>
              </v-list>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
      <v-flex xs12 md3>
        <v-card :class="$style.card" elevation="0" class="transparent">
          <v-layout align-center justify-center column>
            <v-flex xs12>
              <div :class="$style.heading">Important Links</div>
              <br />
              <div :class="['mx-5 mt-4 transparent', $style.text]">
                <router-link to="/career"
                  ><p>Career (work from home)</p></router-link
                >
                <router-link to="/faq"><p>FAQs</p></router-link>
                <router-link to="/question-banks"
                  ><p>Question Banks</p></router-link
                >
                <router-link to="/exams"
                  ><p v-if="userType == 'student'">Exams</p></router-link
                >
                <router-link :to="`/${userType}/dashboard`"
                  ><p v-if="loggedIn">Dashboard</p></router-link
                >
                <router-link to="/terms"><p>Terms & Conditions</p></router-link>
              </div>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
      <v-flex
        class="transparent py-3 primary--text"
        text-xs-center
        xs12
      >
        <v-icon small color="primary">mdi-copyright</v-icon>
        2019 eTests <br/>
        <strong>All rights reserved</strong>
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
  computed: {
    userType() {
      return this.$store.state.authentication.user.type;
    },
    loggedIn() {
      return this.$store.state.authentication.status.loggedIn;
    }
  },
  components: {
    SectionLayout
  }
};
</script>

<style module lang="stylus">
.card{
   margin: 25px 0px;
   border-radius: 15px;
   max-width: 98%;
   height: 90%;
   padding: 10px 0px;
   .sticker{
     position: relative;
     top: -50px;
   }

   .heading{
     font-family: 'Open Sans';
     font-size: 1.4rem;
   }
   .text{
      margin: 15  px auto;
      max-width: 400px;
      font-family: 'Montserrat';
      font-size: 0.95rem;
     p{
      text-align: justify;
     }
   }
}
</style>
