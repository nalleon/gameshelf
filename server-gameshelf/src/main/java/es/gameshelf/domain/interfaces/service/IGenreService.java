package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Genre;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IGenreService {
    Genre add(String name);
    List<Genre> findAll();
    Genre findById(Integer id);
    Genre findByName(String name);
    boolean delete(Integer id);
    Genre update(Integer id, String name);
}
