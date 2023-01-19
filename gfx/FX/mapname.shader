Includes = {
	"sharedconstants.fxh"
	"jomini/countrynames.fxh"
	"distance_fog.fxh"
	"fog_of_war.fxh"
	# MOD(colorful-mapname)
	"coloroverlay.fxh"
	# END MOD
}

VertexShader =
{
	MainCode MapNameVertexShader
	{
		Input = "VS_INPUT_MAPNAME"
		Output = "VS_OUTPUT_MAPNAME"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_MAPNAME Out = MapNameVertexShader( Input, FlatMapHeight, FlatMapLerp );
				return Out;
			}
		]]
	}
}

PixelShader =
{
	TextureSampler FontAtlas
	{
		Ref = PdxTexture0
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}

	MainCode MapNamePixelShader
	{
		Input = "VS_OUTPUT_MAPNAME"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float Alpha = CalcAlphaDistanceField( FontAtlas, Input.TexCoord );
				float3 Color = float3( 0.0f, 0.0f, 0.0f );

                // All credits to terrapass for this shader code
				static const float3 TARGET_COUNTRY_COLOR = float3(0.0f, 0.0f, 9.0f)/255.0f; // Country we want to change
                static const float3 TARGET_MAPNAME_COLOR = float3(1.0f, 1.0f, 1.0f); // Full black

				float2 ProvinceCoords = Input.WorldSpacePos.xz / ProvinceMapSize;
				float4 CountryColor   = BilinearColorSample( ProvinceCoords, IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture );

				if (distance(CountryColor, TARGET_COUNTRY_COLOR) < 0.012f) { // Tweak the distance comparison value to get it working
					Color = lerp(Color, TARGET_MAPNAME_COLOR, FlatMapLerp);
                    Alpha *= lerp(1.0f, 0.5f, FlatMapLerp);
                }

				float3 FlatmapColor = Color; // Pre effects color

				// Fog of war
				Color = ApplyFogOfWar( Color, Input.WorldSpacePos );

				// Flatmap color
				Color = lerp( Color, FlatmapColor, FlatMapLerp);

				return float4( Color, Alpha );
			}
		]]
	}
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
	WriteMask = "RED|GREEN|BLUE"
}

RasterizerState RasterizerState
{
	frontccw = yes
}

DepthStencilState DepthStencilState
{
	DepthEnable = no
}


Effect mapname
{
	VertexShader = "MapNameVertexShader"
	PixelShader = "MapNamePixelShader"
}

