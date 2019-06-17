<template>
  <div class="section">
    <v-layout row wrap fill-height :class="$style.hero">
      <v-flex xs12>
        <div :class="$style.heading">
          eTests
        </div>
        <div :class="$style.subheading" xs12>
          enhance your potential
        </div>
      </v-flex>
      <v-flex xs12>
        <v-carousel light cycle hide-delimiters class="elevation-0">
          <v-carousel-item
            v-for="(feature, i) in features"
            :key="i"
            :class="$style.carouselItem"
          >
            <v-layout row wrap>
              <v-flex xs12 md6>
                <v-img :src="feature.src" :class="$style.img" />
              </v-flex>

              <v-flex xs12 md6 :class="$style.title">
                <p :class="`${feature.color}--text`">
                  {{ feature.title }}
                </p>
                <v-flex xs12 :class="$style.btn">
                  <v-btn round outline large :color="feature.color">
                    {{ feature.btn.title }}
                    <v-icon right dark>
                      {{ feature.btn.icon }}
                    </v-icon>
                  </v-btn>
                </v-flex>
              </v-flex>
            </v-layout>
          </v-carousel-item>
        </v-carousel>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: "Exams",
  data() {
    return {
      features: [
        {
          title: "Adopted by many",
          src: require("@assets/images/features/useful.png"),
          btn: {
            icon: "mdi-account-plus",
            title: "register now"
          },
          color: "info"
        },
        {
          title: "Useful analytics for self assesment",
          src: require("@assets/images/features/analytics.png"),
          btn: {
            icon: "mdi-youtube",
            title: "watch a demo"
          },
          color: "success"
        },
        {
          title: "Effective pricing",
          src: require("@assets/images/features/money.png"),
          btn: {
            icon: "mdi-currency-usd",
            title: "see our plans"
          },
          color: "orange"
        }
      ]
    };
  }
};
</script>

<style module lang="stylus">
.hero {
    padding-top: 50px;
    background-color: #fefeff;
    font-family: "Product Sans Light";
    .heading{
        margin-top: 30px;
        font-size: 3rem;
    }
    .subheading{
        font-size: 1.6rem;
        text-transform: uppercase
        margin-bottom: 10px;
    }
    .carouselItem{
        .title{
            font-size: 1.5rem
            margin-top: 50px;

        }
        .btn{
            margin-top: 20px;
        }
        .img{
            width: 50%;
            margin: auto;
        }
    }
}


.logo{
  width: 30px;
  float: left;
  margin: 0 5px;
}
</style>
