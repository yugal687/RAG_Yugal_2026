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

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const cleanedQuestion = question.trim();

    if (!cleanedQuestion || loading) {
      return;
    }

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: cleanedQuestion,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ]);

    setQuestion("");
    setLoading(true);
    setError("");

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

      const result = data as AskResponse;

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: result.answer,
        sources: result.sources,
      };

      setMessages((currentMessages) => [
        ...currentMessages,
        assistantMessage,
      ]);
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
    setMessages([]);
    setQuestion("");
    setError("");
  }

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-8 text-slate-100">
      <div className="mx-auto flex min-h-[calc(100vh-4rem)] max-w-5xl flex-col">
        <header className="mb-6 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-blue-400">
            Local RAG Application
          </p>

          <h1 className="mt-2 text-3xl font-bold sm:text-5xl">
            Nepal History Assistant
          </h1>

          <p className="mx-auto mt-3 max-w-2xl text-slate-400">
            Ask questions about the indexed document. Answers are grounded in
            retrieved Pinecone context.
          </p>
        </header>

        <section className="flex flex-1 flex-col overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-xl">
          <div className="flex-1 space-y-6 overflow-y-auto p-5 sm:p-7">
            {messages.length === 0 && (
              <div className="flex min-h-[380px] items-center justify-center">
                <div className="max-w-lg text-center">
                  <h2 className="text-2xl font-semibold">
                    Start a conversation
                  </h2>

                  <p className="mt-3 text-slate-400">
                    Ask a question such as:
                  </p>

                  <button
                    type="button"
                    onClick={() =>
                      setQuestion(
                        "Who began the campaign to unify Nepal?"
                      )
                    }
                    className="mt-5 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-300 transition hover:border-blue-500 hover:text-white"
                  >
                    Who began the campaign to unify Nepal?
                  </button>
                </div>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={
                  message.role === "user"
                    ? "flex justify-end"
                    : "flex justify-start"
                }
              >
                <div
                  className={
                    message.role === "user"
                      ? "max-w-[85%] rounded-2xl rounded-br-md bg-blue-600 px-5 py-4 text-white"
                      : "max-w-[90%] rounded-2xl rounded-bl-md border border-slate-700 bg-slate-950 px-5 py-4"
                  }
                >
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider opacity-70">
                    {message.role === "user" ? "You" : "Assistant"}
                  </p>

                  <p className="whitespace-pre-wrap leading-7">
                    {message.content}
                  </p>

                  {message.role === "assistant" &&
                    message.sources &&
                    message.sources.length > 0 && (
                      <div className="mt-5 border-t border-slate-800 pt-4">
                        <p className="mb-3 text-sm font-semibold text-blue-300">
                          Retrieved sources
                        </p>

                        <div className="space-y-3">
                          {message.sources.map((source, index) => (
                            <details
                              key={`${message.id}-${source.chunk_number}-${index}`}
                              className="rounded-xl border border-slate-800 bg-slate-900"
                            >
                              <summary className="cursor-pointer list-none p-4">
                                <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
                                  <div>
                                    <p className="text-sm font-semibold">
                                      {source.source}
                                    </p>

                                    <p className="mt-1 text-xs text-slate-400">
                                      Chunk {source.chunk_number}
                                    </p>
                                  </div>

                                  <span className="w-fit rounded-full bg-blue-950 px-3 py-1 text-xs text-blue-300">
                                    Score: {source.score.toFixed(4)}
                                  </span>
                                </div>
                              </summary>

                              <div className="border-t border-slate-800 px-4 py-3">
                                <p className="whitespace-pre-wrap text-sm leading-6 text-slate-300">
                                  {source.text}
                                </p>
                              </div>
                            </details>
                          ))}
                        </div>
                      </div>
                    )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="rounded-2xl rounded-bl-md border border-slate-700 bg-slate-950 px-5 py-4">
                  <p className="text-sm text-slate-400">
                    Generating Answer...
                  </p>
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="border-t border-red-900 bg-red-950/40 px-5 py-3 text-sm text-red-200">
              {error}
            </div>
          )}

          <form
            onSubmit={handleSubmit}
            className="border-t border-slate-800 bg-slate-900 p-4 sm:p-5"
          >
            <div className="flex flex-col gap-3 sm:flex-row">
              <textarea
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="Ask a question about the document..."
                rows={2}
                maxLength={500}
                disabled={loading}
                className="flex-1 resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-slate-100 outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-60"
              />

              <div className="flex gap-3 sm:flex-col">
                <button
                  type="submit"
                  disabled={loading || !question.trim()}
                  className="flex-1 rounded-xl bg-blue-600 px-6 py-3 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:bg-slate-700"
                >
                  {loading ? "Working..." : "Send"}
                </button>

                <button
                  type="button"
                  onClick={clearConversation}
                  disabled={loading || messages.length === 0}
                  className="rounded-xl border border-slate-700 px-5 py-3 font-semibold text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Clear
                </button>
              </div>
            </div>

            <p className="mt-2 text-right text-xs text-slate-500">
              {question.length}/500
            </p>
          </form>
        </section>
      </div>
    </main>
  );
}