<template>
    <StandardLayout>
        <v-flex xs12 >
            <header class="al-hero-header">
                    <div class="al-hero-cta">
                        <div class="text-xs-left">
                            <h1 class="al-cta-title">Let's Make Conducting Online Exams Easier</h1>
                                <p class="al-cta-desc">eTests is Online Testing platform that supports diferent pattern of exams including JEE Mains, JEE Advance, NEET UG, AIMS. We provide a complete solution to create Test for batches of institute or create and sell question banks. Join Us and Work from your own city. </p>
                                <p class="al-cta-desc">Roles and Responsibilites</p>
                                <ul>
                                    <li>Contact Institutes and Communicate them about our services.</li>
                                    <li>Help the institute for creation and conduction on tests Hazzle Free.</li>
                                </ul>
                                <br/>
                            </div>
                            <v-btn round color="white" @click="toggleDialog">
                                <template v-if="!dialog.length">
                                    Join Now
                                </template>
                                <template v-else>
                                    Close
                                </template>
                            </v-btn>
                            <v-expansion-panel class="elevation-0" v-model="dialog" expand>
                                <v-expansion-panel-content class="transparent" hide-actions>
                                    <v-card class="transparent elevation-0">
                                    <v-card-text>
                                        <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSc1lTSlKR6X0Re4mHkUFd4Ixp0zAGrvj3-UUGSbjs2X_0Ay9Q/viewform?embedded=true" width="640" height="1594" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
                                    </v-card-text>
                                    </v-card>
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                    </div>
                    <svg class="al-wave" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 1240 120" style="enable-background:new 0 0 1240 120;" xml:space="preserve">
                        <path class="hk" d="M682.2,39.6C418.5-11.1,140.2,9.9,0,30v96h1440V30C1252.7,52.2,1011,96.4,675.6,38.7z" fill="#ffffff" />
                    </svg>
            </header>
    </v-flex>
    </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";

  export default {
    data () {
      return {
        dialog: []
      }
    },
    methods: {
      toggleDialog() {
        if(!this.dialog.length) this.dialog = [...Array(this.items).keys()].map(_ => true);
        else this.dialog = [];
      }
    },
    components: {
    StandardLayout
  }
  }
</script>

<style scoped>
 .al-hero-header {
     background-image: linear-gradient(to right, #28CC9E, #196B69);
     background-size:cover;
     background-repeat:no-repeat;
     background-position:center center;
     background-attachment:fixed;
}
 .al-hero-cta {
     font-family: "Product Sans Light";
     max-width:750px;
     margin:0 auto;
     padding:140px 30px 140px 30px 
}
 .al-hero-cta .al-cta-title {
     font-family: "Product Sans Light";
     color:#fff;
     padding-top:50px;
     font-weight:900;
     font-size:42px;
}
 .al-hero-cta .al-cta-desc,ul,li {
     font-family: "Product Sans Light";
     color:#fff;
     font-size:20px;
}

</style>
