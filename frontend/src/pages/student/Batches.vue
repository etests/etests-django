<template>
  <StandardLayout>
    <v-dialog v-if="batches" v-model="joinDialog" max-width="400">
      <v-card :class="$style.joinDialog">
        <v-card-title :class="$style.title">
          Join {{ batches[batchIndex].name }}
        </v-card-title>
        <template v-if="joining">
          <v-card-text>
            Please wait...
          </v-card-text>
        </template>
        <template v-else-if="joined">
          <v-card-text>
            Joined successfully!
          </v-card-text>
        </template>
        <template v-else>
          <v-card-text>
            Enter your joining credentials.
          </v-card-text>
          <v-layout wrap px-4>
            <v-flex xs12>
              <v-text-field
                label="Roll Number"
                v-model="rollNumber"
                required
              ></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                label="Joining Key"
                v-model="joiningKey"
                required
              ></v-text-field>
            </v-flex>
          </v-layout>
        </template>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="info" flat @click="joinDialog = false">
            Close
          </v-btn>
          <v-btn
            v-if="!joining && !joined"
            color="info"
            @click="join(batchIndex)"
          >
            Join
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-layout row wrap v-if="batches">
      <v-flex xs12 md4 v-for="(batch, i) in batches" :key="i">
        <v-card :class="$style.batchCard">
          <v-img
            class="white--text"
            height="170px"
            src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
          >
            <v-card-title class="align-end fill-height">
              {{ batch.name }}
            </v-card-title>
          </v-img>

          <v-card-actions>
            <v-btn
              flat
              color="info"
              @click="
                batchIndex = i;
                joinDialog = true;
              "
            >
              Join
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import SectionLayout from "@components/layouts/SectionLayout";

export default {
  data() {
    return {
      batchIndex: 0,
      rollNumber: "",
      joiningKey: "",
      joinDialog: false,
      rollNumbers: ""
    };
  },
  components: {
    StandardLayout,
    SectionLayout
  },
  created() {
    this.$store.dispatch("batches/detailedList");
  },
  computed: {
    batches() {
      return this.$store.state.batches.all.items;
    },
    joining() {
      return this.$store.state.batches.status.joining;
    },
    joined() {
      return this.$store.state.batches.status.joined;
    }
  },
  methods: {
    join(i) {
      var data = {
        batch: this.batches[i].pk,
        rollNumber: this.rollNumber,
        joiningKey: this.joiningKey
      };
      this.$store.dispatch("batches/join", data);
    }
  }
};
</script>

<style module lang="stylus">

.joinDialog{
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
  text-align: left;
  .title{
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #5e5766;
  }
  .listBox{
    margin: 10px auto 5px;
    padding: 10px;
    width: 100%;
    height: 300px;
    border: 1px solid #999;
    border-radius: 5px;
  }
}

.batchCard{
    text-align: center;
    border-radius: 8px;
    height: 220px;
    width: 250px;
}
</style>
