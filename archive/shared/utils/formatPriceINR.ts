export const formatPriceINR = (value: number, type: "sale" | "rent") => {
  if (type === "rent") return `₹${value.toLocaleString()} /month`
  if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)}Cr`
  if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`
  return `₹${value.toLocaleString()}`
}
