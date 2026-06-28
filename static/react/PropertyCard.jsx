import React from 'react';

/**
 * PropertyCard - Polished premium luxury real estate card component
 * Designed with a sharp rectangular flat layout, zero rounded corners, and a corporate luxury feel.
 * Color Scheme:
 * - Primary: Navy Blue (#0E2A47)
 * - Accent: Mustard Gold (#C89B2B)
 * NOTE: All action buttons have been removed. This is an informational-only card.
 */
export default function PropertyCard({
  imageUrl = '/static/images/propertism-hero-bg.webp',
  badge = 'Exclusive Portfolio',
  name = 'The Grand Pavilion Villa',
  location = 'East Coast Road (ECR), Chennai',
  price = '₹4.85 Crore',
  configuration = '4 BHK Beach Villa',
  area = '4,200 Sq.Ft.',
  builder = 'Signature Estates Group',
  highlights = ['Sea-Facing Vista', 'Private Infinity Pool', 'State-of-the-art Automation', 'Ready to Occupy'],
}) {
  return (
    <div className="w-full bg-white border border-[#0E2A47]/10 flex flex-col md:flex-row relative transition-all duration-300 hover:border-[#C89B2B]/40 select-none text-left rounded-none">
      
      {/* Property Image Area - Sharp Rectangular Layout & Refined Image Ratio */}
      <div className="relative w-full md:w-[35%] aspect-[16/10] md:aspect-auto overflow-hidden bg-[#F7F8FA] min-h-[180px]">
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-full object-cover transition-transform duration-500 hover:scale-105 rounded-none"
          onError={(e) => {
            e.target.src = 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80';
          }}
        />
        {/* Premium Badge */}
        {badge && (
          <div className="absolute top-0 left-0 bg-[#C89B2B] text-white text-[9px] font-bold tracking-widest uppercase px-3 py-1 font-sans">
            {badge}
          </div>
        )}
      </div>

      {/* Property Details Area - Enhanced Typography & Visual Spacing */}
      <div className="w-full md:w-[65%] p-4 md:p-5 flex flex-col justify-between bg-white">
        <div>
          {/* Header Info */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-1.5 mb-2.5">
            <div>
              <h4 className="text-sm font-bold text-[#0E2A47] font-sans tracking-tight uppercase leading-tight">
                {name}
              </h4>
              <p className="text-[10px] text-gray-500 font-sans tracking-wide mt-0.5">
                {location}
              </p>
            </div>
            <div className="text-sm font-bold text-[#C89B2B] font-sans whitespace-nowrap self-start md:self-center">
              {price}
            </div>
          </div>

          <hr className="border-t border-[#0E2A47]/5 my-2.5" />

          {/* Key Specs Table Grid - Polished Metadata Alignment */}
          <div className="grid grid-cols-3 gap-2 text-left mb-3">
            <div className="border-r border-[#0E2A47]/5 pr-1.5">
              <span className="block text-[8px] uppercase tracking-wider text-gray-400 font-sans">
                Config
              </span>
              <span className="block text-[10px] font-semibold text-[#0E2A47] font-sans truncate">
                {configuration}
              </span>
            </div>
            <div className="border-r border-[#0E2A47]/5 px-1.5">
              <span className="block text-[8px] uppercase tracking-wider text-gray-400 font-sans">
                Area
              </span>
              <span className="block text-[10px] font-semibold text-[#0E2A47] font-sans truncate">
                {area}
              </span>
            </div>
            <div className="pl-1.5">
              <span className="block text-[8px] uppercase tracking-wider text-gray-400 font-sans">
                Builder
              </span>
              <span className="block text-[10px] font-semibold text-[#0E2A47] font-sans truncate">
                {builder}
              </span>
            </div>
          </div>

          {/* Highlights List */}
          {highlights && highlights.length > 0 && (
            <div className="mb-1">
              <span className="block text-[8px] uppercase tracking-wider text-gray-400 font-sans mb-1">
                Highlights
              </span>
              <div className="flex flex-wrap gap-1">
                {highlights.map((item, idx) => (
                  <span
                    key={idx}
                    className="text-[9px] font-medium text-[#0E2A47] bg-[#F7F8FA] border border-[#0E2A47]/5 px-2 py-0.5 uppercase tracking-wider font-sans whitespace-nowrap"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
