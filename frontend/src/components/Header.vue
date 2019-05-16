<template>
  <v-layout>
    <v-navigation-drawer
      clipped
      app
      v-model="drawer"
      :temporary="temporaryDrawer"
    >
      <v-list>
        <template v-for="(item, i) in menu">
          <v-divider v-if="item.divider" :key="i" dark class="my-3"></v-divider>
          <v-list-tile v-else :key="i" @click="$router.push(item.link)">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      color="primary"
      tabs
      dark
      app
      clipped-left
      :scroll-off-screen="!drawer"
      :scroll-threshold="10"
      :flat="offsetTop == 0"
    >
      <v-toolbar-side-icon @click="drawer = !drawer">
        <v-icon>mdi-menu</v-icon>
      </v-toolbar-side-icon>

      <router-link :to="{ name: 'home' }">
        <v-toolbar-title class="white--text headline">
          <img
            src="~@assets/logos/etests_light.png"
            :class="[$style.logo, 'hidden-sm-and-down']"
          />
          <span><strong>eTests</strong></span>
        </v-toolbar-title>
      </router-link>

      <v-spacer />

      <slot name="tools">
        <v-text-field
          solo-inverted
          flat
          hide-details
          label="Search"
          prepend-inner-icon="mdi-magnify"
          class="hidden-sm-and-down"
        ></v-text-field>

        <v-menu bottom left>
          <template v-slot:activator="{ on }">
            <v-btn icon v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>

          <v-list>
            <v-list-tile
              v-for="(item, i) in dotMenu"
              :key="i"
              @click="$router.push('#')"
            >
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
      </slot>

      <template v-slot:extension>
        <slot name="tabs"></slot>
      </template>
    </v-toolbar>
  </v-layout>
</template>

<script>
export default {
  props: {
    showDrawer: {
      required: false,
      default: null,
      type: Boolean
    },
    temporaryDrawer: {
      required: false,
      default: false,
      type: Boolean
    }
  },
  data() {
    return {
      offsetTop: 0,
      drawer: this.showDrawer,
      title: "eTests",
      slogan: "an online testing platform",

      menu: [
        { title: "Home", icon: "mdi-home", link: { name: "home" } },

        { divider: "true" },

        { title: "Profile", icon: "mdi-account", link: { name: "profile" } },
        {
          title: "Progress Report",
          icon: "mdi-chart-line",
          link: { name: "report" }
        },

        { divider: "true" },

        {
          title: "Exam Schedule",
          icon: "mdi-note-text",
          link: { name: "exams" }
        },
        {
          title: "Institutes",
          icon: "mdi-school",
          link: { name: "institutes" }
        },
        {
          title: "Test",
          icon: "mdi-desktop-mac-dashboard",
          link: { name: "test" }
        },
        {
          title: "Discuss",
          icon: "mdi-account-group",
          link: { name: "discuss" }
        },
        { divider: "true" },
        {
          title: "Login",
          icon: "mdi-key-variant",
          link: { name: "auth", params: { authType: 2 } }
        },
        {
          title: "Register",
          icon: "mdi-account-plus",
          link: { name: "auth", params: { authType: 0 } }
        }
      ],
      dotMenu: [{ title: "Login" }, { title: "Register" }]
    };
  },
  mounted() {
    window.onscroll = () => {
      this.offsetTop = window.scrollY;
    };
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.logo{
  width: 40px;
  float: left;
  margin: 0 5px;
}
</style>
