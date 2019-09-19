<template>
  <StandardLayout>
    <v-dialog v-model="followDialog" max-width="400">
      <v-card :class="$style.dialog">
        <v-card-title :class="$style.title">Follow {{ selectedInstitute.name }}</v-card-title>
        <template v-if="status.following && status.id === selectedInstitute.id">
          <v-card-text>Please wait...</v-card-text>
        </template>
        <template v-else-if="status.followed && status.id === selectedInstitute.id">
          <v-card-text>{{ status.message }}</v-card-text>
        </template>
        <template v-else>
          <v-card-text>
            After following this institute, you can follow a batch and then
            attempt live tests.
          </v-card-text>
        </template>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="info" flat @click="followDialog = false">Close</v-btn>
          <v-btn
            v-if="
              (!status.following && !status.followed) ||
                !status.id ||
                status.id !== selectedInstitute.id
            "
            color="info"
            @click="follow(selectedInstitute.id)"
          >Follow</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-if="selectedTestSeries"
      v-model="viewDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="viewDialog = false">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>{{ selectedTestSeries.name }}</v-toolbar-title>
        </v-toolbar>
        <v-layout row wrap align-center pa-3>
          <ObjectCard v-for="test in selectedTestSeries.tests" :key="test.id">
            <div slot="content" :class="$style.content">
              <div :class="$style.title">{{ test.name }}</div>
              <v-divider class="my-3" />
              <v-icon color="blue" small>mdi-calendar</v-icon>
              {{ formatDate(test.activation_time) }}
            </div>
            <div slot="actions">
              <v-card-actions>
                <v-layout row fill-height py-2>
                  <v-flex xs4>
                    <v-btn large color="primary" flat round>{{ test.time_alotted }}</v-btn>
                  </v-flex>
                </v-layout>
              </v-card-actions>
            </div>
          </ObjectCard>
        </v-layout>
      </v-card>
    </v-dialog>
    <v-dialog
      v-if="selectedInstitute"
      v-model="instituteDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="instituteDialog = false">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>{{ selectedInstitute.name }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <template v-if="loggedIn">
            <v-btn
              color="blue"
              v-if="showFollowing(selectedInstitute.id)"
              flat
              @click="followDialog = true"
            >Follow</v-btn>
          </template>
        </v-toolbar>
        <v-layout row wrap align-center pa-3>
          <ObjectCard v-for="testSeries in selectedInstitute.test_series" :key="testSeries.id">
            <div slot="content" :class="$style.content">
              <div :class="$style.title">
                {{ testSeries.name }}
                <br />
              </div>
              <v-divider class="my-3" />
              <v-icon color="blue" small>mdi-file-outline</v-icon>
              {{ testSeries.tests.length }} tests ({{ testSeries.exam }})
            </div>
            <div slot="actions">
              <v-card-actions>
                <v-layout row fill-height py-2>
                  <v-flex xs4>
                    <v-btn large color="blue" flat>&#8377; {{ testSeries.price }}</v-btn>
                  </v-flex>

                  <v-flex xs4>
                    <v-btn round outline color="primary">Buy</v-btn>
                  </v-flex>
                  <v-flex xs4>
                    <v-btn
                      round
                      outline
                      color="primary"
                      @click="
                        selectedTestSeries = testSeries;
                        viewDialog = true;
                      "
                    >View</v-btn>
                  </v-flex>
                </v-layout>
              </v-card-actions>
            </div>
          </ObjectCard>
        </v-layout>
      </v-card>
    </v-dialog>
    <v-flex xs12>
      <v-text-field placeholder="Search Institutes" v-model="searchInstitute" />
    </v-flex>

    <v-card
      v-for="institute in filteredInstitutes"
      :key="institute.id"
      @click="
        selectedInstitute = institute;
        instituteDialog = true;
      "
      :class="$style.card"
    >
      <v-img class="white--text" height="170px" :src="institute.src" />
      <v-card-title class="subheading">{{ institute.name }}</v-card-title>
    </v-card>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import ObjectCard from "@/components/layouts/ObjectCard";
import { mapState } from "vuex";
import utils from "@/js/utils";

export default {
  data() {
    return {
      instituteDialog: false,
      viewDialog: false,
      searchInstitute: "",
      filteredInstitutes: [],
      followDialog: false,
      selectedInstitute: {},
      selectedTestSeries: {}
    };
  },
  components: {
    StandardLayout,
    ObjectCard
  },
  created() {
    this.$store.dispatch("institutes/getAll");
  },
  watch: {
    searchInstitute: function(newValue, oldValue) {
      this.filteredInstitutes = this.institutes.filter(institute =>
        institute.name.toLowerCase().includes(newValue)
      );
    },
    institutes: function(newList, oldList) {
      if (this.filteredInstitutes.length === 0)
        this.filteredInstitutes = this.institutes;
    }
  },
  computed: {
    ...mapState({
      status: state => state.institutes.status,
      loggedIn: state => state.authentication.status.loggedIn,
      user: state => state.users.user
    }),
    institutes() {
      var list = [];
      if (this.$store.state.institutes.all.items) {
        this.$store.state.institutes.all.items.forEach(function(item) {
          list.push({
            id: item.id,
            ...item.user,
            test_series: item.test_series,
            src:
              "https://d2mpqlmtgl1znu.cloudfront.net/AcuCustom/Sitename/DAM/011/news-buildings-jan18-dnaiot.jpg"
          });
        });
      }
      return list;
    }
  },
  methods: {
    formatDate(dateString) {
      return utils.formatDate(dateString);
    },
    follow(id) {
      this.$store.dispatch("institutes/follow", id);
    },
    showFollowing(id) {
      if (
        this.loggedIn &&
        this.user &&
        this.user.details &&
        this.user.details.following &&
        !this.user.details.following.includes(id)
      )
        return true;
      else return false;
    }
  },
  mounted() {}
};
</script>

<style module lang="stylus">
@require '~@/stylus/theme/colors';

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

.card {
  text-align: center;
  border-radius: 8px;
  height: 220px;
  width: 270px;
  margin: 10px;
  cursor: pointer;
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
