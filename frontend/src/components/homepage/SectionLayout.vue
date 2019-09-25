<template>
  <div class="section">
    <v-layout
      fill-height
      :class="[$style.section, !isSmallScreen ? $style.space : '']"
    >
      <v-flex xs12 align-end flexbox>
        <div :class="$style.heading">
          <slot name="heading"></slot>
        </div>
        <div :class="$style.subheading">
          <slot name="subheading"></slot>
        </div>
        <v-layout row justify-center wrap>
          <slot name="content"></slot>
        </v-layout>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSmallScreen: this.$vuetify.breakpoint.smAndDown
    };
  }
};
</script>
<style module lang="stylus">
@require '~@/stylus/theme/colors';
.section{
  padding: 70px 10px 20px;

  .heading{
    font-family: "Open Sans";
    font-weight: 800;
    font-size: 2.1rem;
  }

  .subheading{
      font-family: "Montserrat";
      font-weight: 600;
      font-size: 1.2rem;
  }
}
.space{
  padding-top: 8%;
}
</style>

<style scoped>
.section:nth-child(even) {
  background-color: #f5f5f5;
}
</style>
