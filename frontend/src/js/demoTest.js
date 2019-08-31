export const demoSession = {
  response: [
    { answer: [], status: 1, timeElapsed: 7 },
    { answer: [], status: 1, timeElapsed: 103 },
    { answer: [], status: 1, timeElapsed: 158 },
    { answer: [], status: 1, timeElapsed: 654 }
  ],
  test: {
    name: "test1",
    slug: "test1",
    active: true,
    practice: false,
    date_added: "2019-08-17",
    activation_time: "2019-08-29",
    time_alotted: "03:00:00",
    sections: [
      { end: 2, start: 0, subject: "Subject 1" },
      { end: 3, start: 3, subject: "Biology" }
    ],
    questions: [
      {
        text: "How are You?",
        type: 0,
        image: null,
        status: 3,
        answers: ["Answer P", "Answer Q", "Answer R", "Answer S", "Answer T"],
        options: ["Fine", "Option B", "Option C", "Option D"],
        section: 0,
        correctMarks: 4,
        incorrectMarks: 1
      },
      {
        text: "Traits of venkat.",
        type: 1,
        image: null,
        status: 3,
        answers: ["Answer P", "Answer Q", "Answer R", "Answer S", "Answer T"],
        options: ["Chutiya", "Bsdike", "gandu", "BCMC"],
        section: 0,
        correctMarks: 4,
        incorrectMarks: 1
      },
      {
        text: "hdjgf",
        type: 2,
        image: null,
        status: 3,
        answers: ["Answer P", "Answer Q", "Answer R", "Answer S", "Answer T"],
        options: ["Option A", "Option B", "Option C", "Option D"],
        section: 0,
        correctMarks: 4,
        partialMarks: 0,
        incorrectMarks: 1
      },
      {
        text: "",
        type: 0,
        image: null,
        status: 3,
        answers: ["Answer P", "Answer Q", "Answer R", "Answer S", "Answer T"],
        options: ["Male", "Female", "Gay", "Lesbian"],
        section: 1,
        correctMarks: 4,
        incorrectMarks: 1
      }
    ],
    answers: [
      { answer: 0 },
      { answer: [0, 1, 2, 3] },
      { answer: "45" },
      { answer: 2 }
    ],
    institute: 1,
    registered_student: [1, 2],
    tags: []
  },
  duration: "3:00:00",
  current: { questionIndex: 0, sectionIndex: 0 },
  completed: false
};
