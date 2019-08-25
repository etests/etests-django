import { reviewService } from "@/api/review.service";

const initialState = {
  status: {},
  review: null
};

export const reviews = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }, id) {
      commit("getRequest", id);
      reviewService.get(id).then(
        review => {
          commit("getSuccess", review);
        },
        error => {
          commit("getFailure", error);
        }
      );
    }
  },
  mutations: {
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, review) {
      state.status = { exists: true };
      state.review = review;
    },
    getFailure(state, error) {
      state.status = { error };
    }
  }
};
