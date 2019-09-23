<template>
  <SectionLayout>
    <v-layout row wrap justify-center slot="content">
      <v-flex xs12 md3>
        <v-card :class="$style.card"    elevation="0" class="transparent">
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
                eTests is the new standard in online testing solutions. Number of Institutes conducts their exams and create and sell their
                Question Banks on etests. Students from all over india preparing for pre-engineering and pre-medical examinations are geting benifit from our services.
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
    
         <v-flex xs12 md3>
        <v-card :class="$style.card" elevation="0" class="transparent">
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
              <h3>Let Us Help You</h3>
              <v-list class="transparent">
                <h4>100% support</h4>
                <v-list-tile-content>
                <v-list-tile-title class="subheading" >For student</v-list-tile-title>
               <p>You can Practice all types of 
                 questions including Single Correct, Multiple Correct, Integer Types, Matrix Match for your Competitive exams. After the 
                 completion of exam the detailed analysis of your performance using pie charts and bar graphs are generated. You can review each
                 question and responses made by you including the time you spent on each question during the test. We promise to give you 100% support in the services. Any technical issue raised regarding exams or question banks or any
                  payment made by you will be resolved within 24 hrs.</p>
              </v-list-tile-content>
               <v-list-tile-content>
                <v-list-tile-title class="subheading" >For Institutes</v-list-tile-title>
               <p>Our online testing platform is developed and tested by team of IITians. We have support for wide range of examination pattern
                 There is special support for Pre-Engineering(including JEE Mains And JEE Advance) and Premedical( including NEET and AIMS) exams.
                 You can create test for your batches or question banks using our test editor. The text editor provides MS word like text editor for creating 
                 questions. Apart from this you can also send us the pdf of test papers for creation of your tests. We promise to resolve any technical issue within 
                 24 hrs.
               </p>
              </v-list-tile-content>
            </v-list-tile>
              </v-list>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
        <v-flex xs12 md3>
        <v-card :class="$style.card" elevation="0" class="transparent">
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
              <p>Careers(Work From Home)</p>
              <p>FAQs</p>
              <p>Question Banks</p>
              <p>Dashboard</p>
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
   margin: 25px 0px;
   border-radius: 15px;
   max-width: 98%;
   height: 90%;
   padding: 10px 0px;
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
