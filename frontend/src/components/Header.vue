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
          <div
            v-if="
              (item.requiresStudent && isStudent) ||
                (item.requiresInstitute && isInstitute) ||
                (!item.requiresStudent && !item.requiresInstitute)
            "
            :key="i"
          >
            <v-divider v-if="item.divider" dark class="my-2"></v-divider>
            <v-list-tile
              :to="item.link"
              :class="$style.DrawerItem"
              :active-class="$style.activeDrawerItem"
              v-else
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
          </div>
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
        v-if="!disableDrawerClose || isSmallScreen"
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
          v-if="showSearchBar"
        ></v-text-field>

        <template v-else>
          <v-toolbar-items class="hidden-sm-and-down">
            <v-btn
              flat
              color="#1a916f"
              v-for="item in topNavMenu"
              :key="item.title"
              :to="item.link"
            >
              {{ item.title }}
            </v-btn>
          </v-toolbar-items>

          <v-spacer />
        </template>
      </slot>

      <v-dialog v-model="showLoginDialog" max-width="600px">
        <Login />
      </v-dialog>

      <v-menu bottom left transition="slide-y-transition">
        <template v-slot:activator="{ on }">
          <v-btn flat color="primary" icon v-on="on">
            <v-icon large>mdi-account-circle</v-icon>
          </v-btn>
        </template>

        <v-list>
          <span v-for="(item, i) in dotMenu" :key="i">
            <v-list-tile
              :to="item.link"
              @click="item.action"
              v-if="item.requiresLogin == loggedIn"
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
          </span>
        </v-list>
      </v-menu>

      <template v-slot:extension>
        <slot name="tabs"></slot>
      </template>
    </v-toolbar>
  </v-layout>
</template>

<script>
import Login from "./Login";

export default {
  props: {
    isAbsolute: {
      reuired: false,
      default: false,
      type: Boolean
    },
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
    },
    showSearchBar: {
      required: false,
      default: true,
      type: Boolean
    }
  },
  data() {
    return {
      offsetTop: 0,
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      drawer: this.showDrawer,
      title: "eTests",
      slogan: "an online testing platform",
      showLoginDialog: false,
      topNavMenu: [
        { title: "Home", icon: "mdi-home-outline", link: { name: "home" } },

        {
          title: "Institutes",
          icon: "mdi-domain",
          link: { name: "institutes" }
        },
        {
          title: "Tests",
          icon: "mdi-note-multiple-outline",
          link: { path: "/institute/tests" },
          requiresInstitute: true
        },

        {
          title: "Discuss",
          icon: "mdi-account-group-outline",
          link: { name: "discuss" }
        }
      ],
      menu: [
        { title: "Home", icon: "mdi-home-outline", link: { name: "home" } },

        {
          title: "Institutes",
          icon: "mdi-domain",
          link: { name: "institutes" }
        },

        { divider: true },

        {
          title: "Dashboard",
          icon: "mdi-view-dashboard-outline",
          link: { path: "/student/dashboard" },
          requiresStudent: true
        },
        {
          title: "Progress Report",
          icon: "mdi-chart-line",
          link: { name: "report" },
          requiresStudent: true
        },

        {
          title: "Exam Schedule",
          icon: "mdi-calendar-text-outline",
          link: { name: "exams" },
          requiresStudent: true
        },
        {
          title: "Test",
          icon: "mdi-monitor-screenshot",
          link: { name: "test" },
          requiresStudent: true
        },

        { divider: true, requiresStudent: true },

        {
          title: "Dashboard",
          icon: "mdi-view-dashboard-outline",
          link: { path: "/institute/dashboard" },
          requiresInstitute: true
        },
        {
          title: "Tests",
          icon: "mdi-note-multiple-outline",
          link: { path: "/institute/tests" },
          requiresInstitute: true
        },
        {
          title: "Notifications",
          icon: "mdi-bell-ring-outline",
          link: { path: "/institute/notifications" },
          requiresInstitute: true
        },

        { divider: true, requiresInstitute: true },

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
          link: "",
          action: _ => {
            return (this.showLoginDialog = true);
          },
          requiresLogin: false
        },
        {
          title: "Register",
          icon: "mdi-account-plus-outline",
          link: "",
          action: _ => {
            return (this.showLoginDialog = true);
          },
          requiresLogin: false
        },
        {
          title: "Profile",
          icon: "mdi-account-outline",
          link: { name: "profile" },
          action: _ => {
            return false;
          },
          requiresLogin: true
        },
        {
          title: "Logout",
          icon: "mdi-logout-variant",
          link: "",
          action: this.logout,
          requiresLogin: true
        }
      ]
    };
  },
  components: {
    Login
  },
  methods: {
    logout() {
      if (this.loggedIn) this.$store.dispatch("authentication/logout");
    }
  },
  computed: {
    loggedIn() {
      if (this.$store.state.authentication.status.loggedIn) return true;
      return false;
    },
    isStudent() {
      if (!this.loggedIn) return false;
      return this.$store.state.authentication.user.is_student;
    },
    isInstitute() {
      if (!this.loggedIn) return false;
      return this.$store.state.authentication.user.is_institute;
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

.dotMenu{

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

<style scoped>
.v-menu__content {
  border-radius: 8px;
  font-family: "Product Sans Light";
  font-size: 1.3rem;
  min-width: 160px;
}
</style>
