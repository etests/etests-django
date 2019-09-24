export const testTemplate = {
  name: "New Test",
  sections: [
    {
      subject: "Subject 1",
      start: 0,
      end: 0,
      subjectIndex: 0
    }
  ],
  questions: [
    {
      section: 0,
      text:
        "<p>Enter question text and options or insert image here.</p><p>&nbsp;</p>",
      type: 0,
      status: 1,
      correctMarks: 4,
      incorrectMarks: 1,
      partialMarks: 0,
      topic: "",
      topicIndex: 0,
      options: ["A", "B", "C", "D"],
      answers: ["P", "Q", "R", "S", "T"]
    }
  ],
  answers: [{ answer: [], solution: "<p>Enter the solution text or image here.</p>" }]
};
