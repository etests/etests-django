<template>
  <StandardLayout>
    <v-flex xs12 md4>
      <v-card :class="[$style.dashboardCard, $style.profile, 'px-4']">
        <div :class="$style.profilePicContainer">
          <v-img
            src="https://picsum.photos/id/11/500/300"
            lazy-src="https://picsum.photos/id/11/10/6"
            aspect-ratio="1"
            :class="$style.profilePic"
          />
        </div>
        <v-btn
          round
          color="primary"
          depressed
          style="width: 100%; margin: auto"
        >
          {{ this.profile.name.value }}
        </v-btn>
        <v-divider class="my-3"></v-divider>
        <v-flex xs12 md12 class="pb-4">
          <v-sheet>
            <v-list>
              <v-list-tile v-for="item in profile" :key="item.title">
                <v-layout row align-center wrap>
                  <v-flex xs2>
                    <v-list-tile-action>
                      <v-icon>{{ item.icon }}</v-icon>
                    </v-list-tile-action>
                  </v-flex>

                  <v-flex xs4>
                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{ item.title }}
                      </v-list-tile-title>
                    </v-list-tile-content>
                  </v-flex>

                  <v-flex xs6>
                    <v-list-tile-content>
                      <span v-if="!editing">
                        {{ item.value }}
                      </span>
                      <span v-else>
                        <input
                          :class="$style.textbox"
                          type="text"
                          v-model="item.value"
                        />
                      </span>
                    </v-list-tile-content>
                  </v-flex>
                </v-layout>
              </v-list-tile>
            </v-list>
            <v-layout column align-center>
              <v-flex xs12>
                <v-fab-transition>
                  <v-btn
                    @click="editing = !editing"
                    color="primary"
                    dark
                    fab
                    absolute
                    right
                  >
                    <v-icon v-if="!editing">mdi-lead-pencil</v-icon>
                    <v-icon v-else>mdi-content-save</v-icon>
                  </v-btn>
                </v-fab-transition>
              </v-flex>
            </v-layout>
          </v-sheet>
        </v-flex>

        <v-divider class="mt-2"></v-divider>

        <v-flex xs12 md12 v-if="profile.account">
          <v-sheet>
            <v-list>
              <v-list-tile
                v-for="item in profile.account.items"
                :key="item.title"
              >
                <v-layout row align-center wrap>
                  <v-flex xs2>
                    <v-list-tile-action>
                      <v-icon>{{ item.icon }}</v-icon>
                    </v-list-tile-action>
                  </v-flex>
                  <v-flex xs5>
                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{ item.title }}
                      </v-list-tile-title>
                    </v-list-tile-content>
                  </v-flex>
                  <v-flex xs5>
                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{ item.detail }}
                      </v-list-tile-title>
                    </v-list-tile-content>
                  </v-flex>
                </v-layout>
              </v-list-tile>
            </v-list>
          </v-sheet>
        </v-flex>
      </v-card>
    </v-flex>
    <v-flex xs12 md8>
      <v-card :class="[$style.dashboardCard, 'px-2 py-2']">
        <v-container grid-list-sm fluid>
          <v-layout row wrap>
            <v-flex
              v-for="control in controls"
              :key="control.name"
              xs6
              sm4
              lg3
              xl2
            >
              <v-card flat tile class="d-flex">
                <v-layout column align-center justify-center>
                  <v-flex xs12>
                    <v-img
                      :class="$style.control"
                      :src="control.image"
                      aspect-ratio="1"
                      width="100"
                      class="my-4"
                      @click="$router.push(control.link)"
                    />
                  </v-flex>
                  <v-flex xs12>
                    <v-spacer></v-spacer>
                    <div class="subheading">{{ control.name }}</div>
                  </v-flex>
                </v-layout>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-flex>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";

export default {
  props: ["profile", "controls"],
  data() {
    return {
      editing: false
    };
  },
  components: {
    StandardLayout
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.dashboardCard{
    text-align: left;
    border: 1px solid #c9cbd0;
    border-radius: 8px;
    margin: 30px 15px;
    margin-top: 70px;
    font-family: "Product Sans Light";
    box-shadow: 2px 5px 15px #ccc;
}

.profile{
    .profilePicContainer{
      position: relative;
        height: 100px;
        width: 100%;
        text-align: center;

      .profilePic{
        box-shadow: 0px 2px 10px #999;
        position: absolute;
        left: calc( 50% - 75px );
        top: -70px;
        border-radius: 100%;
        height: 150px;
        width: 150px;
        margin: auto;
      }
    }

}

.control{
    border-radius: 100%;
    cursor: pointer
}
.textbox{
    width:100%;
    height:100%;
    padding: 12px 8px;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    position: relative;
}
</style>
