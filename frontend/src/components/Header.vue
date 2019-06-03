<template>
  <v-layout>
    <v-navigation-drawer
      clipped
      app
      v-model="drawer"
      floating
      width="260"
      :temporary="temporaryDrawer"
    >
      <v-list>
        <template v-for="(item, i) in menu">
          <v-divider v-if="item.divider" :key="i" dark class="my-2"></v-divider>
          <v-list-tile
            v-else
            :key="i"
            :to="item.link"
            :class="$style.DrawerItem"
            :active-class="$style.activeDrawerItem"
          >
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title :class="$style.drawerItemTitle">
                {{ item.title }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      color="white"
      tabs
      app
      clipped-left
      :scroll-off-screen="!drawer"
      :scroll-threshold="10"
      :flat="offsetTop == 0"
    >
      <v-toolbar-side-icon
        v-if="!disableDrawerClose || !drawer"
        @click="drawer = !drawer"
      >
        <v-icon color="primary">mdi-menu</v-icon>
      </v-toolbar-side-icon>

      <router-link :to="{ name: 'home' }">
        <v-toolbar-title class="headline">
          <img src="~@assets/logos/etests.png" :class="$style.logo" />
          <span><strong>eTests</strong></span>
        </v-toolbar-title>
      </router-link>

      <v-spacer />

      <slot name="tools">
        <v-text-field
          flat
          solo-inverted
          hide-details
          label="Search eTests"
          prepend-inner-icon="mdi-magnify"
          clear-icon="mdi-close"
          clearable
          :class="['hidden-sm-and-down', $style.searchBox]"
        ></v-text-field>
      </slot>

      <v-menu bottom left min-width="150">
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-tile
            v-for="(item, i) in dotMenu"
            :key="i"
            :to="item.link"
            @click="item.action"
          >
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.title }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-menu>

      <template v-slot:extension>
        <slot name="tabs"></slot>
      </template>
    </v-toolbar>
  </v-layout>
</template>

<script>
export default {
  props: {
    disableDrawerClose: {
      reuired: false,
      default: false,
      type: Boolean
    },
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
        { title: "Home", icon: "mdi-home-outline", link: { name: "home" } },

        {
          title: "Institutes",
          icon: "mdi-domain",
          link: { name: "institutes" }
        },

        { divider: "true" },

        {
          title: "Dashboard",
          icon: "mdi-view-dashboard-outline",
          link: { name: "student-dashboard" }
        },
        {
          title: "Progress Report",
          icon: "mdi-chart-line",
          link: { name: "report" }
        },

        {
          title: "Exam Schedule",
          icon: "mdi-calendar-text-outline",
          link: { name: "exams" }
        },
        {
          title: "Test",
          icon: "mdi-monitor-screenshot",
          link: { name: "test" }
        },

        { divider: "true" },

        {
          title: "Discuss",
          icon: "mdi-account-group-outline",
          link: { name: "discuss" }
        }
      ],
      dotMenu: [
        {
          title: "Login",
          icon: "mdi-key-outline",
          link: { name: "auth", params: { authType: 2 } },
          action: _ => {
            return false;
          }
        },
        {
          title: "Register",
          icon: "mdi-account-plus-outline",
          link: { name: "auth", params: { authType: 0 } },
          action: _ => {
            return false;
          }
        },
        {
          title: "Profile",
          icon: "mdi-account-outline",
          link: { name: "profile" },
          action: _ => {
            return false;
          }
        },
        {
          title: "Logout",
          icon: "mdi-logout-variant",
          link: "",
          action: this.logout
        }
      ]
    };
  },
  methods: {
    logout() {
      if (this.$store.state.authentication.status.loggedIn)
        this.$store.dispatch("authentication/logout");
    }
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
  width: 30px;
  float: left;
  margin: 0 5px;
}


.DrawerItem{
  a{
    border-radius: 0 50px 50px 0;
  }
  .drawerItemTitle{
      letter-spacing: .06em;
      font-size: 0.95rem;
      word-break: break-word;
      word-wrap: break-word;
  }
}

.activeDrawerItem {
    background: $aero;
    color: $genoa;
}
</style>
