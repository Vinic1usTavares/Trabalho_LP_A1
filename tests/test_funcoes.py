import pandas as pd
import os
import sys
import unittest

# Adiciona o diretório 'src' ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import funcoes as func

class TestFuncoes(unittest.TestCase):

    def test_abrir_arquivo_csv(self):
        self.assertIsInstance(func.abrir_anime_csv('data/anime.csv'), pd.DataFrame)
        self.assertRaises(FileNotFoundError,func.abrir_anime_csv(),'caminho_errado')

    def test_filtrar_generos(self):
        data = {
            'genre': ['Adventure', 'Isekai', 'Hentai', 'Harem'],
            'episodes': ['1', '23', '4', '90']
        }
        df = pd.DataFrame(data)
        df = func.filtrar_generos(df)
        self.assertEqual(len(df['genre']), 2)
    
    def test_convert_date(self):
        self.assertEqual(func.convert_date('Jan 02, 2004'), '02/01/2004')
        

    def test_limpar_dados(self):
        df = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'name': ['Anime A', 'Anime B', 'Anime C', 'Anime D'],
            'type': ['Movie', 'TV', None, 'Movie'],
            'episodes': ['unknown', '10', '20', None],
            'rating': [8.0, None, 7.5, 9.0],
            'genre': [['Action'], ['Drama'], None, ['Comedy']],
            'members': [1000, None, 1500, 2000],
            'aired': ['2020', None, '2021', '2022']
        })
        cleaned_df = func.limpar_dados(df)
        self.assertEqual(cleaned_df.shape[0], 2)
        self.assertEqual(cleaned_df.loc[cleaned_df['id'] == 1, 'episodes'].values[0], 1)
        self.assertNotIn(2, cleaned_df['id'].values)


    def test_remover_unknown(self):
        df = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Anime A', 'Anime B', 'Anime C', 'Anime D'],
        'episodes': ['10', 'unknown', '20', 'unknown']
    })
    
        cleaned_df = func.remover_unknown(df)

        # Verifica se as linhas com 'unknown' foram removidas
        self.assertEqual(cleaned_df.shape[0], 2)
        self.assertNotIn('unknown', cleaned_df['episodes'].values)
    
    def test_processar_anime(self):
        func.processar_anime()
        self.assertTrue(os.path.exists('data/anime_filtrado_limpo.csv'))

    def test_extrair_ano(self):
        self.assertEqual(func.extrair_ano('12/08/2015'), 2015)
        self.assertEqual(func.extrair_ano('01/01/2000'), 2000)
        self.assertEqual(func.extrair_ano('31/12/1999'), 1999)
        

if __name__ == '__main__':
    unittest.main()