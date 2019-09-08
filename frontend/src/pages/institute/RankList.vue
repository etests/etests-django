<template>
  <v-data-table v-if="rankList" :headers="rankHeaders" :items="ranks">
    <template v-slot:items="props">
      <td class="text-xs-center">{{ props.item.overall }}</td>
      <td class="text-xs-center">{{ props.item.roll_number }}</td>
      <td class="text-xs-center">{{ props.item.name }}</td>
    </template>
  </v-data-table>
</template>

<script>
export default {
  props: ["rankList"],
  data() {
    return {
      rankHeaders: [
        {
          align: "center",
          sortable: true,
          text: "Rank",
          value: "overall"
        },
        {
          align: "center",
          sortable: true,
          text: "Roll Number",
          value: "roll_number"
        },
        { align: "center", sortable: true, text: "Name", value: "name" }
      ]
    };
  },
  computed: {
    ranks() {
      return this.rankList.ranks.map(session => {
        return {
          roll_number: session.roll_number,
          name: session.name,
          ...session.ranks
        };
      });
    }
  }
};
</script>
