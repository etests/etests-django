<template>
    <ObjectCard>
        <div slot="content" :class="$style.content">
            <div :class="$style.title">
            {{ testSeries.name }}
            <br />
            <span class="body-1 mx-1">{{ testSeries.institute.name }}</span>
            </div>
            <v-divider class="my-3" />
            <v-layout row wrap>
            <v-flex xs8>
            <v-icon color="blue" small>mdi-file-outline</v-icon>
            {{ testSeries.tests.length }} tests 
            <span v-if="testSeries.exams.length">
              ({{ testSeries.exams.join(", ") }})
            </span>
            </v-flex>
            <v-flex xs4 class="blue--text subheading">
                &#8377; {{ testSeries.price }}
            </v-flex>
            </v-layout>
        </div>
        <v-layout slot="actions" row fill-height py-2>
            <Payment
            :dialog="paymentDialog"
            :testSeries="testSeries"
            @close="paymentDialog = false"
          />
          <v-dialog
            v-model="viewDialog"
            fullscreen
            hide-overlay
            transition="slide-x-transition"
          >
            <v-card>
              <v-toolbar dark color="primary">
                <v-btn icon dark @click="viewDialog = false">
                  <v-icon v-if="outerParent">mdi-arrow-left</v-icon>
                  <v-icon v-else>close</v-icon>
                </v-btn>
                <v-toolbar-title>
                  <span v-if="outerParent">
                    {{ outerParent }}
                    <v-icon>mdi-chevron-right</v-icon>
                  </span>
                  {{ testSeries.name }}
                </v-toolbar-title>
              </v-toolbar>
              <v-layout row wrap align-center pa-3>
                <ObjectCard v-for="test in testSeries.tests" :key="test.id">
                  <div slot="content" :class="$style.content">
                    <v-card-title :class="$style.title">{{ test.name }}</v-card-title>
                    <v-divider class="mb-3 mx-3" />
                    <v-icon color="blue" class="ml-3" small>mdi-calendar</v-icon>
                    {{ formatDate(test.activation_time) }}
                  </div>
                  <div slot="actions">
                    <v-card-actions>
                      <v-layout row fill-height py-2>
                        <v-flex xs4>
                          <v-btn large color="primary" flat round>{{
                            test.time_alotted
                          }}</v-btn>
                        </v-flex>
                      </v-layout>
                    </v-card-actions>
                  </div>
                </ObjectCard>
              </v-layout>
            </v-card>
          </v-dialog>
            <v-flex xs6>
            <v-btn
                round
                outline
                color="primary"
                v-if="loggedIn && user.type=='student'"
                @click="
                testSeries = testSeries;
                paymentDialog = true;
                "
            >
                Buy
            </v-btn>
            <v-btn
                round
                outline
                color="primary"
                v-else-if="!loggedIn"
                disabled
            >
                Login to Buy
            </v-btn>
            </v-flex>
            <v-flex xs6>
            <v-btn
                round
                outline
                color="primary"
                @click="
                testSeries = testSeries;
                viewDialog = true;
                "
                >
                  View
                </v-btn>
            </v-flex>
        </v-layout>
    </ObjectCard>
</template>

<script>
import ObjectCard from "@/components/layouts/ObjectCard";
import Payment from "./Payment";
import { mapState } from "vuex";
import utils from "@/js/utils";

export default {
  props: {
    testSeries: {
      required: true,
      type: Object
    },
    outerParent: {
      required: false,
      type: String
    }
  },
  data() {
    return {
      paymentDialog: false,
      viewDialog: false,
    };
  },
  components: {
    ObjectCard,
    Payment
  },
  computed: {
    ...mapState({
      loggedIn: state => state.authentication.status.loggedIn,
      user: state => state.users.user
    })
  },
  methods: {
    formatDate(dateString) {
      return utils.formatDate(dateString);
    }
  }
};
</script>

<style module lang="stylus">
.card {
  text-align: center;
  border-radius: 8px;
  height: 220px;
  width: 270px;
  margin: 10px;
  cursor: pointer;
}

.dialog {
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light', Roboto, Arial, sans-serif;
  text-align: left;

  .title {
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #5e5766;
  }
}

.content {
  padding: 20px;
  min-height: 160px;
  background-color: #fafafa;
  border-radius: 8px 8px 0 0;
  text-align: left;

  &:hover {
    background-color: #f5f5f5;
  }
}

.title {
  text-align: left;
  font-size: 1.375rem;
  line-height: 1.75rem;
  color: #7e777e;
}
</style>
