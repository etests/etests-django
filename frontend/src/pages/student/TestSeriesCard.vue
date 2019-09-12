<template>
  <ObjectCard>
    <div slot="content" :class="$style.content">
      <v-progress-circular
        :size="70"
        :width="7"
        color="grey darken-1"
        indeterminate
        v-if="loading"
        class="mt-5"
      ></v-progress-circular>

      <template v-else>
        <div :class="$style.title">
          {{ testSeries.name }} <br />
          <span class="body-1 mx-1">{{ testSeries.institute.name }}</span>
        </div>
        <v-divider class="my-3" />
        <v-icon color="blue" small>mdi-file-outline</v-icon>
        {{ testSeries.tests.length }} tests ({{ testSeries.exam }})
      </template>
    </div>
    <div slot="actions">
      <v-card-actions>
        <v-layout row>
          <template v-if="this.showActions">
            <v-flex xs6>
              <v-btn large color="blue" flat>
                &#8377; {{ testSeries.price }}
              </v-btn>
            </v-flex>

            <v-flex xs6>
              <v-btn round outline color="primary" @click="$emit('viewTests')">
                View
              </v-btn>
            </v-flex>
          </template>
        </v-layout>
      </v-card-actions>
    </div>
  </ObjectCard>
</template>

<script>
import ObjectCard from "@components/layouts/ObjectCard";
import { mapState } from "vuex";

export default {
  props: {
    testSeries: {
      required: false,
      default: () => {
        return { name: "", description: "", new: true };
      },
      type: Object
    },
    new: {
      required: false,
      default: false,
      type: Boolean
    }
  },
  data() {
    return {
      loading: false,
      viewDialog: false,
      showActions: !this.new
    };
  },
  computed: {
    ...mapState({
      status: state => state.testSeries.status
    })
  },
  components: {
    ObjectCard
  },
  methods: {},
  mounted() {}
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.content{
  padding: 20px;
  min-height: 160px;
  background-color: #fcfcfc;
  border-radius: 8px 8px 0 0;
  text-align: left;
  &:hover{
      background-color: #f5f5f5;
  }
  }

.title, .editTitle{
  text-align: left;
  font-size: 1.375rem;
  line-height: 1.75rem;
  color: #7e777e;
}

.editTitle, .editDescription{
  padding: 12px 15px 0;
  margin: 0;
  input{
    color: #7e777e !important;
    letter-spacing: 0.06rem;
    border-color: #eee !important;
  }
}

.description, .editDescription{
  letter-spacing: .014em;
  text-align: left;
  font-size: 0.9rem;
  line-height: 1.25rem;
  color: #5f6368;
}
</style>
