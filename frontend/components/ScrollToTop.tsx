'use client'

import {useState, useEffect} from 'react'

export default function ScrollToTop() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setVisible(window.scrollY >= 300)
    }
    window.addEventListener('scroll', handleScroll, {passive: true})
    handleScroll()
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const scrollToTop = () => {
    window.scrollTo({top: 0, behavior: 'smooth'})
  }

  return (
    <button
      onClick={scrollToTop}
      aria-label="ページ上部に戻る"
      className={`fixed bottom-6 right-6 z-40 flex items-center justify-center w-10 h-10 rounded-full bg-[#292929] text-white shadow-lg hover:bg-[#444] transition-opacity duration-300 cursor-pointer ${
        visible ? 'opacity-100' : 'opacity-0 pointer-events-none'
      }`}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M18 15l-6-6-6 6" />
      </svg>
    </button>
  )
}
