# A tiny survey, used to show off Ruby colors.
require "json"

module Demo
  class Survey
    MAX_ANSWERS = 25
    attr_reader :title

    def initialize(title, anonymous: true)
      @title = title
      @anonymous = anonymous
      @answers = []
    end

    def add(text, score: nil)
      raise ArgumentError, "blank answer" if text.to_s.strip.empty?
      @answers << { text: text, score: score }
      self
    end

    def average
      scores = @answers.map { |a| a[:score] }.compact
      scores.empty? ? 0.0 : scores.sum / scores.size
    end
  end
end

survey = Demo::Survey.new("Favorite theme")
survey.add("Warm", score: 0.9).add("Cream paper", score: 0.8)
puts "#{survey.title}: #{survey.average.round(2)}"
puts JSON.generate(title: survey.title, ok: true)
