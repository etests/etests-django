<template>
  <StandardLayout>
    <v-dialog v-if="loggedIn" v-model="joinDialog" max-width="400">
      <v-card :class="$style.dialog">
        <v-card-title :class="$style.title">
          Follow {{ selectedInstitute.name }}
        </v-card-title>
        <template v-if="status.joining && status.id === selectedInstitute.id">
          <v-card-text>
            Please wait...
          </v-card-text>
        </template>
        <template
          v-else-if="status.joined && status.id === selectedInstitute.id"
        >
          <v-card-text>
            {{ status.message }}
          </v-card-text>
        </template>
        <template v-else>
          <v-card-text>
            After following this institute, you can join a batch and then
            attempt live tests.
          </v-card-text>
        </template>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="info" flat @click="joinDialog = false">
            Close
          </v-btn>
          <v-btn
            v-if="
              (!status.joining && !status.joined) ||
                !status.id ||
                status.id !== selectedInstitute.id
            "
            color="info"
            @click="join(selectedInstitute.id)"
          >
            Follow
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-flex xs12>
      <v-text-field placeholder="Search Institutes" v-model="searchInstitute" />
    </v-flex>
    <ObjectCard v-for="institute in filteredInstitutes" :key="institute.id">
      <div slot="content" :class="$style.content">
        <v-img :src="institute.src" height="200px">
          <template v-slot:placeholder>
            <v-layout fill-height align-center justify-center ma-0>
              <v-progress-circular
                indeterminate
                color="grey"
              ></v-progress-circular>
            </v-layout>
          </template>
        </v-img>
      </div>
      <div slot="actions">
        <v-card-actions>
          <v-container fill-height fluid pa-2>
            <v-layout fill-height>
              <v-flex xs12 align-end flexbox>
                <span class="body1" v-text="institute.name"></span>
              </v-flex>
            </v-layout>
          </v-container>
          <v-spacer></v-spacer>
          <v-btn
            color="blue"
            v-if="showFollowing(institute.id)"
            flat
            @click="
              selectedInstitute = institute;
              joinDialog = true;
            "
          >
            Follow
          </v-btn>
        </v-card-actions>
      </div>
    </ObjectCard>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import ObjectCard from "@components/layouts/ObjectCard";
import { mapState } from "vuex";

export default {
  data() {
    return {
      searchInstitute: "",
      filteredInstitutes: [],
      joinDialog: false,
      selectedInstitute: {}
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
      var institutes = this.institutes;
      this.filteredInstitutes = institutes.filter(institute =>
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
      user: state => state.authentication.user
    }),
    institutes() {
      var list = [];
      if (this.$store.state.institutes.all.items) {
        this.$store.state.institutes.all.items.forEach(function(item) {
          list.push({
            id: item.pk,
            name: item.user.name,
            src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg"
          });
        });
      }
      return list;
    }
  },
  methods: {
    join(id) {
      this.$store.dispatch("institutes/follow", id);
    },
    showFollowing(id) {
      if (
        this.loggedIn &&
        this.user.type === "student" &&
        !this.user.student.following.includes(id)
      )
        return true;
      else return false;
    }
  },
  mounted() {}
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.dialog{
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
  text-align: left;
  .title{
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #5e5766;
  }
}

.content{
  min-height: 160px;
  background-color: #fcfcfc;
  border-radius: 8px 8px 0 0;
  text-align: center;
  &:hover{
      background-color: #f5f5f5;
  }
}
</style>
