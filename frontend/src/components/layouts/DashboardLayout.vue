<template>
  <StandardLayout>
    <v-card :class="[$style.card, 'elevation-3']">
      <v-layout row wrap>
        <v-flex xs12 md4>
          <v-card :class="[$style.dashboardCard, $style.profile, 'px-4 elevation-0']">
            <div :class="$style.profilePicContainer">
              <v-img
                src="http://vyfhealth.com/wp-content/uploads/2015/10/yoga-placeholder1.jpg"
                aspect-ratio="1"
                :class="$style.profilePic"
              />
            </div>
            <v-divider class="my-3" />
            <v-flex xs12 md12>
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
            </v-flex>
          </v-card>
        </v-flex>
        <v-flex xs12 md8>
          <v-card class="elevation-0 pa-1">
            <v-container grid-list-sm fluid>
              <v-layout row wrap>
                <v-flex
                  v-for="control in controls"
                  :key="control.name"
                  xs6
                >
                  <v-card flat tile class="d-flex">
                    <v-layout column align-center justify-center>
                      <v-flex xs12>
                        <v-img
                          :class="$style.control"
                          :src="control.image"
                          aspect-ratio="1"
                          width="100"
                          class="my-3"
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
      </v-layout>
    </v-card>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";

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
@require '~@/stylus/theme/colors';

.card{
  width: 100%;
  margin: 0 20px;
  padding: 20px 5px;
  border-radius: 8px;
}

.dashboardCard{
    margin-top: 70px;
}

.profile{
    .profilePicContainer{
      position: relative;
        height: 100px;
        width: 100%;
        text-align: center;

      .profilePic{
        box-shadow: 0px 2px 2px #999;
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
