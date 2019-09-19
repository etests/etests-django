<template>
  <StandardLayout>
    <SectionLayout heading="Transactions">
      <v-flex xs12>
        <v-text-field
          v-model="transactionsearch"
          append-icon="search"
          label="Search"
          single-line
        ></v-text-field>
        <v-data-table
          v-if="transcations"
          :headers="transactionheaders"
          :items="transcations"
          :search="transactionsearch"
          class="elevation-1"
        >
          <template v-slot:items="props">
            <td class="text-xs-center">{{ props.item.date_added }}</td>
            <td class="text-xs-center">{{ props.item.amount }}</td>
            <td class="text-xs-center">{{ props.item.credits_added }}</td>
            <td class="text-xs-center">{{ props.item.transaction_id }}</td>
            <td class="text-xs-center">{{ props.item.mode }}</td>
          </template>
        </v-data-table>
      </v-flex>
    </SectionLayout>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>

    <SectionLayout heading="Credit Uses">
      <v-flex xs12>
        <v-text-field
          v-model="creditsearch"
          append-icon="search"
          label="Search"
          single-line
        ></v-text-field>
        <v-data-table
          v-if="creditsUsed"
          :headers="creditheaders"
          :items="creditsUsed"
          :search="creditsearch"
          class="elevation-1"
        >
          <template v-slot:items="props">
            <td class="text-xs-center">{{ props.item.date_added }}</td>
            <td class="text-xs-center">{{ props.item.test }}</td>
            <td class="text-xs-center">{{ props.item.credits_used }}</td>
          </template>
        </v-data-table>
      </v-flex>
      <v-tooltip left>
        <template v-slot:activator="{ on }">
          <v-btn color="primary" dark v-on="on">Left</v-btn>
        </template>
        <span>Left tooltip</span>
      </v-tooltip>
    </SectionLayout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import SectionLayout from "@/components/layouts/SectionLayout";

export default {
  data() {
    return {
      transactionsearch: "",
      creditsearch: "",
      transactionheaders: [
        { align: "center", sortable: true, text: "Date", value: "date_added" },
        {
          align: "center",
          text: "Amount Paid",
          value: "amount",
          sortable: true
        },
        {
          align: "center",
          text: "Credits Added",
          value: "credits_added",
          sortable: true
        },
        {
          align: "center",
          text: "Transaction ID",
          value: "transaction_id",
          sortable: false
        },
        { align: "center", text: "Mode", value: "mode", sortable: true }
      ],
      creditheaders: [
        { align: "center", sortable: true, text: "Date", value: "date_added" },
        {
          align: "center",
          text: "Test",
          value: "test",
          sortable: true
        },
        {
          align: "center",
          text: "Credits Used",
          value: "credits_used",
          sortable: true
        }
      ]
    };
  },
  created() {
    this.$store.dispatch("transactions/get");
    this.$store.dispatch("credits/get");
  },
  computed: {
    transcations() {
      return this.$store.state.transactions.items;
    },
    creditsUsed() {
      return this.$store.state.credits.credits;
    }
  },
  components: {
    StandardLayout,
    SectionLayout
  }
};
</script>
