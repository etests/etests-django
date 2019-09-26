<template>
  <StandardLayout>
    <v-dialog v-model="followDialog" max-width="400">
      <v-card :class="$style.dialog">
        <v-card-title :class="$style.title">
          Follow {{ selectedInstitute.name }}
        </v-card-title>
        <template v-if="status.following && status.id === selectedInstitute.id">
          <v-card-text>Please wait...</v-card-text>
        </template>
        <template
          v-else-if="status.followed && status.id === selectedInstitute.id"
        >
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
          <v-btn color="primary" flat @click="followDialog = false">Cancel</v-btn>
          <v-btn
            v-if="
              (!status.following && !status.followed) ||
                !status.id ||
                status.id !== selectedInstitute.id
            "
            color="primary"
            @click="follow(selectedInstitute.id)"
          >
            Follow
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-if="selectedInstitute"
      v-model="instituteDialog"
      fullscreen
      hide-overlay
      transition="scale-transition"
      origin="top left"
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
              class="white primary--text"
              round
              dark
              flat
              v-if="showFollowing(selectedInstitute.id)"
              @click="followDialog = true"
              >Follow</v-btn
            >
          </template>
        </v-toolbar>
        <v-layout row wrap align-center pa-3>
          <QuestionBankCard
            v-for="testSeries in selectedInstitute.test_series"
            :key="testSeries.id"
            :testSeries="testSeries"
            :outerParent="selectedInstitute.name"
          />
        </v-layout>
      </v-card>
    </v-dialog>

    <v-flex xs12 class="px-3">
      <v-text-field placeholder="Search Institutes" v-model="searchInstitute" />
    </v-flex>

    <template v-if="status.loading">
      <LoadingCard v-for="i in 1" :key="i" />
    </template>

    <ObjectCard
      v-for="institute in filteredInstitutes"
      :key="institute.id"
      :class="$style.card"
        @click="
          selectedInstitute = institute;
          instituteDialog = true;
        "
    >
      <div slot="content" :class="$style.content">
        <div :class="$style.title">{{ institute.name }}</div>
         <v-divider class="my-1" />
        <div class="subheading my-3 text-xs-left">{{institute.city}}, {{institute.state}} - {{institute.pincode}}</div>
      </div>
      <v-layout row slot="actions">
        <v-flex xs6>
        <v-btn
          round
          color="primary"
          outline
          @click="
            selectedInstitute = institute;
            instituteDialog = true;
          "
        >
          Open
        </v-btn>
        </v-flex>
        <v-flex xs6>
        <v-btn
          round
          color="primary"
          outline
          v-if="showFollowing(institute.id)"
          @click="
            selectedInstitute = institute;
            followDialog = true;
          "
        >
          Follow
        </v-btn>
        </v-flex>
      </v-layout>
    </ObjectCard>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import LoadingCard from "@/components/layouts/LoadingCard";
import ObjectCard from "@/components/layouts/ObjectCard";
import QuestionBankCard from "./QuestionBankCard";
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
    QuestionBankCard,
    LoadingCard,
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
            pincode: item.pincode,
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
  font-family: 'Montserrat', Roboto, Arial, sans-serif;
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
  .img{
    cursor: pointer;
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
