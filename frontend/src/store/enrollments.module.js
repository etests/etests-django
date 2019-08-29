import { enrollmentService } from "@/api/enrollment.service";

const initialState = {
  status: {},
  generated: null,
  items: null
};

export const enrollments = {
  namespaced: true,
  state: initialState,
  actions: {
    batchEnroll({ dispatch, commit }, data) {
      commit("batchEnrollRequest");
      enrollmentService.batchEnroll(data).then(
        enrollments => {
          commit("batchEnrollSuccess", enrollments);
        },
        error => {
          commit("batchEnrollFailure", error);
        }
      );
    },
    remove({ dispatch, commit }, id) {
      commit("removeRequest", id);

      enrollmentService.remove(id).then(
        _ => {
          commit("removeSuccess", id);
          setTimeout(() => {
            dispatch("alert/success", "Student removed successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("removeFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    getAll({ dispatch, commit }, data) {
      commit("getAllRequest");
      enrollmentService.getAll(data).then(
        enrollments => {
          commit("getAllSuccess", enrollments);
        },
        error => {
          commit("getAllFailure", error);
        }
      );
    }
  },
  mutations: {
    batchEnrollRequest(state) {
      state.status = { loading: true };
    },
    batchEnrollSuccess(state, enrollments) {
      state.status = { exists: true };
      state.generated = enrollments;
    },
    batchEnrollFailure(state, error) {
      state.status = { error };
    },
    getAllRequest(state) {
      state.status = { loading: true };
    },
    getAllSuccess(state, enrollments) {
      state.status = { exists: true };
      state.items = enrollments;
    },
    getAllFailure(state, error) {
      state.status = { error };
    },
    removeRequest(state, id) {
      state.status = { removing: true, id: id };
    },
    removeSuccess(state, id) {
      state.status = { removed: true, id: id };
    },
    removeFailure(state, error) {
      state.status = { error: error };
    }
  }
};
