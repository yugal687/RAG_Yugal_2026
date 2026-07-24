"use client";

import { FormEvent, useState } from "react";

type Source = {
  source: string;
  chunk_number: number;
  score: number;
  text: string;
};

type AskResponse = {
  question: string;
  answer: string;
  sources: Source[];
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const cleanedQuestion = question.trim();

    if (!cleanedQuestion) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: cleanedQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ?? "The backend could not process your question."
        );
      }

      setResult(data as AskResponse);
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : "Unable to connect to the RAG API.";

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function clearConversation() {
    setQuestion("");
    setResult(null);
    setError("");
  }

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100">
      <div className="mx-auto max-w-4xl">
        <header className="mb-8 text-center">
          <p className="mb-2 text-sm font-semibold uppercase tracking-[0.25em] text-blue-400">
            Local RAG Application
          </p>

          <h1 className="text-3xl font-bold sm:text-5xl">
            Nepal History Assistant
          </h1>

          <p className="mx-auto mt-4 max-w-2xl text-slate-400">
            Ask questions about the indexed document. Answers are generated
            using retrieved Pinecone context and Llama 3.2.
          </p>
        </header>

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl sm:p-7">
          <form onSubmit={handleSubmit}>
            <label
              htmlFor="question"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              Your question
            </label>

            <textarea
              id="question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Example: Who began the campaign to unify Nepal?"
              rows={4}
              maxLength={500}
              disabled={loading}
              className="w-full resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-slate-100 outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:cursor-not-allowed disabled:opacity-60"
            />

            <div className="mt-2 text-right text-xs text-slate-500">
              {question.length}/500
            </div>

            <div className="mt-4 flex flex-col gap-3 sm:flex-row">
              <button
                type="submit"
                disabled={loading || !question.trim()}
                className="flex-1 rounded-xl bg-blue-600 px-5 py-3 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:bg-slate-700"
              >
                {loading ? "Generating answer..." : "Ask question"}
              </button>

              <button
                type="button"
                onClick={clearConversation}
                disabled={loading}
                className="rounded-xl border border-slate-700 px-5 py-3 font-semibold text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
              >
                Clear
              </button>
            </div>
          </form>
        </section>

        {error && (
          <section className="mt-6 rounded-2xl border border-red-900 bg-red-950/40 p-5">
            <h2 className="font-semibold text-red-300">Request failed</h2>
            <p className="mt-2 text-sm text-red-200">{error}</p>
          </section>
        )}

        {result && (
          <div className="mt-8 space-y-6">
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <p className="text-sm font-semibold uppercase tracking-wider text-blue-400">
                Answer
              </p>

              <h2 className="mt-3 text-lg font-semibold text-slate-300">
                {result.question}
              </h2>

              <p className="mt-4 leading-8 text-slate-100">
                {result.answer}
              </p>
            </section>

            <section>
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-bold">Retrieved sources</h2>

                <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">
                  {result.sources.length} chunks
                </span>
              </div>

              {result.sources.length === 0 ? (
                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 text-slate-400">
                  No source chunks were returned.
                </div>
              ) : (
                <div className="space-y-4">
                  {result.sources.map((source, index) => (
                    <details
                      key={`${source.source}-${source.chunk_number}-${index}`}
                      className="group rounded-2xl border border-slate-800 bg-slate-900"
                    >
                      <summary className="cursor-pointer list-none p-5">
                        <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
                          <div>
                            <p className="font-semibold">
                              {source.source}
                            </p>

                            <p className="mt-1 text-sm text-slate-400">
                              Chunk {source.chunk_number}
                            </p>
                          </div>

                          <span className="w-fit rounded-full bg-blue-950 px-3 py-1 text-sm text-blue-300">
                            Score: {source.score.toFixed(4)}
                          </span>
                        </div>
                      </summary>

                      <div className="border-t border-slate-800 px-5 py-4">
                        <p className="whitespace-pre-wrap leading-7 text-slate-300">
                          {source.text}
                        </p>
                      </div>
                    </details>
                  ))}
                </div>
              )}
            </section>
          </div>
        )}
      </div>
    </main>
  );
}